from django.shortcuts import render, get_object_or_404
from users.models import User
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import generics, mixins, filters
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet
from .serializers import HackatonUserSerializer, ListTeamSerializer, UserTeamSerializer, HackatonSerializer, TeamSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import User_Team, Team, Hackaton_User, Hackaton
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from .queries import GetHackaton, GetHackatonUser, GetTeam, GetUserTeam, DeleteUserTeam
import jwt
from app.settings import ALLOWED_HOSTS
from .exceptions import NotFoundHackaton, NotFoundHackatonUser, NotFoundTeam, NotFoundUserTeam, NotFoundInvite, TeamIsFull
from django.core.cache import cache
import uuid
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser


#регистрация пользователя на хакатон по id
class HackatonUserView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        request.data['user'] = request.user.pk
        request.data['hackaton'] = request.data.get('id_hackaton')

        serializer = HackatonUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=200, data={'result':'success'})


class TeamView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user_team = GetUserTeam().get_from_user(user=request.user.pk, 
                                                    id_hackaton=request.data.get('id_hackaton'))
            
        queryset = user_team.team
        serializer = TeamSerializer(queryset)
        return Response(status=200, data={'result':serializer.data})

    #создать команду
    def post(self, request):
        user_hack = GetHackatonUser().get_from_user_hack(user=request.user.pk, 
                                                            id_hackaton=request.data.get('id_hackaton'))
            
        DeleteUserTeam().leave_from_team(user=request.user.pk, 
                                             id_hackaton=request.data.get('id_hackaton'))  
            
        request.data['owner'] = user_hack.pk
        request.data['hackaton'] = request.data['id_hackaton']

        serializer = TeamSerializer(data=request.data)   
        serializer.is_valid(raise_exception=True) 
        serializer.save()

        request.data['team'] = serializer.data['id']
        request.data['user'] = user_hack.pk
        request.data['is_invited'] = False

        serializer = UserTeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        serializer.save()

        return Response(status=200, data={'result':'success'})


#получение списка своей команды по id хакатона
class MyTeamListView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        user = GetUserTeam().get_from_user(user=request.user.pk, id_hackaton=request.data.get('id_hackaton'))
            
        queryset = GetUserTeam().get_list_team(user.team.pk)
        serializer_class = ListTeamSerializer(queryset, many=True)
        return Response(status=200, data={'result':serializer_class.data})
        

#Приглашение в команду
class InviteTeamView(APIView):
    permission_classes = [IsAuthenticated,]
    
    #дать инвайт
    def post(self, request):

        team = GetTeam().get_from_owner_hack(request.user.pk, 
                                            request.data.get('id_hackaton'))
            
        user = GetHackatonUser().get_user_hack_for_invite(request.data.get('user'), 
                                                        request.data.get('id_hackaton'))

        serializer = UserTeamSerializer(data={'user': user.pk, 'team':team.pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200, data={'result':'success'})
    
    #принять инвайт
    def update(self, request):
        user_team = GetUserTeam().get_invited(team=request.data.get('team'), user=request.user.pk)
        list_team = GetUserTeam().get_list_team(team=request.data.get('team'))
        if len(list_team) >= 5:
            return Response(status=404, data={'error':'Команда команда переполнена'})
            
        DeleteUserTeam.leave_from_team(user=request.user.pk, id_hackaton=user_team.user.hackaton.pk)
        user_team.is_invited = False
        user_team.save()
        return Response(status=200, data={'result':'success'})
    
    #Выйти из команды
    def put(self, request):
        DeleteUserTeam().leave_from_team(request.user.pk, 
                            request.data.get('id_hackaton'))
        return Response(status=200, data={'result':'success'})


class KickUserView(APIView):
    permission_classes = [IsAuthenticated,]

    #Удалить юзера из команды
    def delete(self, request):
        DeleteUserTeam().kick_user(user=request.data.get('user'), 
                         id_hackaton=request.data.get('id_hackaton'), 
                         owner=request.user.pk)     
        
        return JsonResponse(status=200, data={'result':'success'})


#получение хакатона по id и списка хакатонов
class HackatonListApi(generics.GenericAPIView, 
                      mixins.CreateModelMixin, 
                      mixins.ListModelMixin):
    serializer_class = HackatonSerializer
    
    def get_queryset(self):
        queryset = Hackaton.objects.all()
        filter = {}
        for i in self.request.data.keys():
            filter[i] = self.request.data[i]
        return queryset.filter(**filter)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class HackatonUrlInvite(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        team = GetTeam().get_from_owner_hack(user=request.user, 
                                             id_hackaton=request.data.get('id_hackaton')) 
               
        key = str(uuid.uuid4())
        cache.set(key, team.pk, 10800)
        return Response(status=200, data={'result':'http://127.0.0.1:8000/api/v1/hackaton/invite_url/?team=' + key})
    
    def get(self, request):
        token = request.GET.get('team')

        id_team =  cache.get(token)
        if id_team is None:
            return Response(status=404, data={'error':'Приглашение в команду устарело'})

        team = GetTeam().get_team(id_team)  
        user_hack = GetHackatonUser().get_from_user_hack(user=request.user.pk, id_hackaton=team.hackaton.pk)

        GetUserTeam().count_users_team(id_team)
            
        DeleteUserTeam().leave_from_team(user=request.user.pk, id_hackaton=team.hackaton.pk)
        serializer = UserTeamSerializer(data={'user': user_hack.pk, 'team':team.pk, 'is_invited':False})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200, data={'result':'success'})
