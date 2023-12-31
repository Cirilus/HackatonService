from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema

from .serializers import HistoryPointSerializer, PointConditionSerializer

from .models import HistoryPoint, PointCondition


# Create your views here.

@extend_schema(description="History Points URLs:", tags=["History Points"])
class HistoryPointByUserCRUD(viewsets.ModelViewSet):
    # получаем все записи или конкретную запись по айдишнику собственному
    permission_classes = [AllowAny, ]
    queryset = HistoryPoint.objects.all()
    serializer_class = HistoryPointSerializer
    '''    #нужно ли добавить проверку при добавлении записи,
            что user к которому привязан указываемый condition совпадает с юзером этого condition
    '''

    @action(detail=True, methods=['get'], )  # может добавить и другие методы?
    def bycondition(self, request, condition_id=None):
        # http://127.0.0.1:8000/api/v1/historypointlist/bycondition/<int:condition_id>/
        # получаем одну уникальную запись по condition_id

        if condition_id is None:
            return Response({"error": "В url Необходимо указать параметр condition_id."},
                            status=status.HTTP_400_BAD_REQUEST)

        queryset = HistoryPoint.objects.filter(condition_id=condition_id)
        serializer = HistoryPointSerializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'], )  # может добавить и другие методы?
    def byuserid(self, request, user_id=None):
        # http://127.0.0.1:8000/api/v1/historypointlist/byuserid/<int:user_id>/
        # получаем все записи которые есть для указанного user_id
        if user_id is None:
            return Response({"error": "В url Необходимо указать параметр user_id."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = HistoryPoint.objects.filter(user_id=user_id)
        serializer = HistoryPointSerializer(queryset, many=True)

        return Response(serializer.data)


@extend_schema(description="Point Conndition URLs:", tags=["Point Conditions"])
class PointConditionByUserCRUD(viewsets.ModelViewSet):
    # получаем все записи или конкретную запись по айдишнику собственному из таблицы PointCondition
    permission_classes = [AllowAny, ]
    queryset = PointCondition.objects.all()
    serializer_class = PointConditionSerializer

    @action(detail=False, methods=['get'], )  # может добавить и другие методы?
    def byuserid(self, request, user_id=None):
        # http://127.0.0.1:8000/api/v1/pointconditionlist/byuserid/<int:user_id>/
        # получаем все записи которые есть для указанного user_id
        if user_id is None:
            return Response({"error": "В url Необходимо указать параметр user_id."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = PointCondition.objects.filter(user_id=user_id)
        serializer = PointConditionSerializer(queryset, many=True)

        return Response(serializer.data)
