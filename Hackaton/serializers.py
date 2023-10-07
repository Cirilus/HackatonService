from rest_framework import serializers
from .models import *


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


class InviteTeamSErializer(serializers.ModelSerializer):
    class Meta:
        model = Team_Invite
        fields = '__all__'
