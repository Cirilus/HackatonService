from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response



from .serializers import HistoryPointSerializer, PointConditionSerializer

from .models import HistoryPoint, PointCondition
# Create your views here.


class HistoryPointByUserCRUD(viewsets.ModelViewSet): #получаем конкретную запись по юзер айди
    permission_classes = [AllowAny, ]
    queryset = HistoryPoint.objects.all()
    serializer_class = HistoryPointSerializer
    lookup_field = 'user_id'

    # http://127.0.0.1:8000/api/v1/historypointlist/bycondition/<int:condition_id>/
    # получаем все записи с опредленным condition_id
    @action(detail=False, methods=['get'],)
    def bycondition(self, request, condition_id=None):

        if condition_id is None:
            return Response({"error": "В url Необходимо указать параметр condition_id."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = HistoryPoint.objects.filter(condition_id=condition_id)
        serializer = HistoryPointSerializer(queryset, many=True)

        return Response(serializer.data)


class PointConditionByUserCRUD(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = PointCondition.objects.all()
    serializer_class = PointConditionSerializer
    lookup_field = 'user_id'


