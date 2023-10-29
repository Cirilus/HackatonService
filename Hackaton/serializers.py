from rest_framework import serializers
from .models import Hackaton_User, User_Team, Hackaton, Team


class HackatonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackaton_User
        fields = '__all__'


class ListTeamSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.user.middle_name')
    email = serializers.CharField(source='user.user.email')

    class Meta:
        model = User_Team
        fields = ('username', 'email')


class UserTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Team
        fields = '__all__'


class HackatonSerializer(serializers.ModelSerializer):
    imageUrl = serializers.ImageField()
    class Meta:
        model = Hackaton
        fields = '__all__'
        

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'