from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from .filters import FeedbackFilter
from .serializers import UserSerializer, FeedbackSerializer
from django.http import JsonResponse
from .queries import GetUser, UserScore
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse, OpenApiRequest
from drf_spectacular.types import OpenApiTypes
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .models import User, Feedback
from rest_framework.decorators import action


@extend_schema(
    tags=["User Views"],
    description='CRUD user',
)
class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        description='Получить свой профиль пользователя',
    )
    def my_profile(self, request):
        queryset = GetUser().get_user(request.user.pk)
        serializer = UserSerializer(queryset)
        return Response(status=200, data={'result': serializer.data})


@extend_schema(
    tags=["User Views"],
    description='Регистрация пользователя',
)
class SignUpView(CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


@extend_schema(description="Feedback URLs: (CRUD для feedback)", tags=["Feedback"])
class FeedbackCRUD(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "status": ["exact", ],
        "create_at": ["date__exact", 'date__gte', 'date__lte']
    }

    # ?create_at__date__lte=2023-01-01, ?create_at__date__gte=2023-01-01, ?create_at__date=2023-01-01,
    # ?status=[New, Current, Completed] - запросы на фильтрацию

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user

        user_id = self.request.user

        contact_back = serializer.validated_data.get('contact_back', None)

        if not contact_back:
            serializer.validated_data['contact_back'] = User.objects.get(email=user_id).email

        super().perform_create(serializer)

    @extend_schema(
        description='получить все записи относящиеся к пользователю с определенным user_id',
    )
    @action(detail=False, methods=['get'], )
    def byuserid(self, request, user_id=None):
        # http://127.0.0.1:8000/api/v1/users/feedbacklist/byuserid/<int:user_id>/
        # получаем все записи которые есть для указанного user_id
        if user_id is None:
            return Response({"error": "введите user_id."}, status=status.HTTP_400_BAD_REQUEST)

        if user_id not in Feedback.objects.values_list('user', flat=True):
            return Response({"error": "записи с таким user_id не существует"}, status=status.HTTP_404_NOT_FOUND)

        queryset = Feedback.objects.filter(user_id=user_id)
        serializer = FeedbackSerializer(queryset, many=True)

        return Response(serializer.data)

    @extend_schema(
        description='удалить все записи относящиеся к пользователю с определенным user_id',
    )
    @action(detail=False, methods=['delete'], )
    def delete_by_userid(self, request, user_id=None):
        # http://127.0.0.1:8000/api/v1/feedback/delete_by_userid/<int:user_id>/
        if user_id is None:
            return Response({"error": "Введите user_id."}, status=status.HTTP_400_BAD_REQUEST)

        feedback_objects = Feedback.objects.filter(user_id=user_id)
        if not feedback_objects.exists():
            return Response({"error": "Записи с таким user_id не существуют"}, status=status.HTTP_404_NOT_FOUND)

        feedback_objects.delete()
        return Response({"success": f"Записи для пользователя с user_id {user_id} удалены."}, status=status.HTTP_200_OK)
