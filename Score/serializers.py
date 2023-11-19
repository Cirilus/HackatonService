from rest_framework import serializers
from .models import HistoryPoint, PointCondition


class HistoryPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryPoint
        fields = ['id', 'user', 'condition', 'count', 'created', ]


class PointConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointCondition
        fields = ['user', 'title', 'id']
