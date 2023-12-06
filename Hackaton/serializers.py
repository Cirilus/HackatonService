from rest_framework import serializers
from .models import Hackaton_User, User_Team, Hackaton, Team, JoinRequest

class HackatonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackaton_User
        fields = '__all__'
    

class ListHackatonUsers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.pk')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Hackaton_User
        fields = ['id', 'first_name', 'last_name', 'email']


class ListTeamSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source='user.user.pk')
    first_name = serializers.CharField(source='user.user.first_name')
    last_name = serializers.CharField(source='user.user.last_name')
    email = serializers.CharField(source='user.user.email')

    class Meta:
        model = User_Team
        fields = ('pk', 'first_name', 'last_name', 'email')


class UserTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Team
        fields = '__all__'


class HackatonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackaton
        fields = '__all__'
        

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class JoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinRequest
        fields = '__all__'