from rest_framework import serializers
from .models import HistoryPoint, PointCondition

class HistoryPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryPoint
        fields = ['user', 'condition', 'count','created','id']

class PointConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointCondition
        fields = ['user', 'title','id']

