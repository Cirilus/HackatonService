from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.http import JsonResponse
from .queries import GetUser, UserScore
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse, OpenApiRequest
from drf_spectacular.types import OpenApiTypes


@extend_schema(
        tags=["User Views"],
        description='CRUD user',
        request=UserSerializer,
        responses={200: UserSerializer},
    )
@extend_schema(tags=['Invite in team'])
class UserView(APIView):

    @permission_classes([AllowAny,])
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({'result':'success'})
    
    @permission_classes([IsAuthenticated,])
    def put(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({'result':'success'})
    
    @extend_schema(
        description='Удаление юзера',
        parameters=[OpenApiParameter(name='id', description='id', required=True, type=int),],
        request=OpenApiRequest(),
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example kick from team', value={'result': 'заебца'}, response_only=True, status_codes=[200]),
                  OpenApiExample(name='Example kick from team', value={'error': 'message'}, response_only=True, status_codes=[404]),
        ],
    )
    def delete(self, request):
        GetUser().delete_user(request.GET.get('id'))
        return JsonResponse({'result':'success'})



