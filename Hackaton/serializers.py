from rest_framework import serializers
from .models import Hackaton_User, User_Team


class HackatonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackaton_User
        fields = '__all__'


class ListTeamSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.user.username')
    email = serializers.CharField(source='user.user.email')

    class Meta:
        model = User_Team
        fields = ('username', 'email')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Team
        fields = '__all__'
