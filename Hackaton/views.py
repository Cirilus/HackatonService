from django.shortcuts import render, get_object_or_404
from users.models import User
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
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
        try:
            user_team = GetUserTeam().get_from_user(user=request.user.pk, 
                                                    id_hackaton=request.data.get('id_hackaton'))
            if user_team is None:
                raise NotFoundUserTeam
            
            queryset = user_team.team
            serializer = TeamSerializer(queryset)
            return Response(status=200, data={'result':serializer.data})
        
        except NotFoundUserTeam:
            return Response(status=404, data={'error':'Вы не состоите в команде'})

    #создать команду
    def post(self, request):
        try:
            user_hack = GetHackatonUser().get_from_user_hack(user=request.user.pk, 
                                                            id_hackaton=request.data.get('id_hackaton'))
            if user_hack is None:
                raise NotFoundHackatonUser
            
            DeleteUserTeam().leave_from_team(user=request.user.pk, 
                                             id_hackaton=request.data.get('id_hackaton'))  
            
            request.data['user'] = user_hack.pk
            request.data['hackaton'] = request.data['id_hackaton']

            serializer = TeamSerializer(data=request.data)   
            serializer.is_valid(raise_exception=True) 
            serializer.save()
            return Response(status=200, data={'result':'success'})
        
        except NotFoundHackatonUser:
            return Response(status=404, data={'error':'Вы не зарегистрированы на хакатон'})


#получение списка своей команды по id хакатона
class MyTeamListView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        try:
        
            user = GetUserTeam().get_from_user(user=request.user.pk, id_hackaton=request.data.get('id_hackaton'))
            if user is None:
                raise NotFoundUserTeam
            
            queryset = GetUserTeam().get_list_team(user.team.pk)
            serializer_class = ListTeamSerializer(queryset, many=True)
            return Response(status=200, data={'result':serializer_class.data})
        
        except NotFoundUserTeam:
            return Response(status=404, data={'error':'Вы не состоите в команде'}) 

#Приглашение в команду
class InviteTeamView(APIView):
    permission_classes = [IsAuthenticated,]
    
    #дать инвайт
    def post(self, request):
        try:
            team = GetTeam().get_from_owner_hack(request.user.pk, 
                                             request.data.get('id_hackaton'))
            if team is None:
                raise NotFoundTeam
            
            user = GetHackatonUser().get_from_user_hack(request.data.get('user'), 
                                                    request.data.get('id_hackaton'))
            if user is None:
                raise NotFoundHackaton

            serializer = UserTeamSerializer(data={'user': user.pk, 'team':team.pk})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=200, data={'result':'success'})
        
        except NotFoundHackatonUser:
            return Response(status=404, data={'error':'Пользователь не найден'})
        except NotFoundTeam:
            return Response(status=404, data={'error':'Вы не являетесь создателем команды'})
    
    #принять инвайт
    def put(self, request):
        try:
            user_team = GetUserTeam().get_invited(team=request.data.get('team'), user=request.user.pk)
            if user_team is None:
                raise NotFoundUserTeam
            
            if GetUserTeam().get_list_team(team=request.data.get('team')) >= 5:
                raise TeamIsFull
            
            DeleteUserTeam.leave_from_team(user=request.user.pk, id_hackaton=user_team.user.hackaton.pk)
            user_team.is_invited = False
            user_team.save()
            return Response(status=200, data={'result':'success'})
        
        except NotFoundUserTeam:
            return Response(status=404, data={'error':'Приглашение не найдено'})
        except TeamIsFull:
            return Response(status=405, data={'error':'Команда переполнена'})
    

    #Выйти из команды
    def delete(self, request):
        if DeleteUserTeam().leave_from_team(request.user.pk, 
                            request.data.get('id_hackaton')):
            
            return Response(status=200, data={'result':'success'})
        return Response(status=405, data={'error':'Не удалось выполнить выход'})

class KickUserView(APIView):
    permission_classes = [IsAuthenticated,]

    #Удалить юзера из команды
    def delete(self, request):
        if DeleteUserTeam().kick_user(user=request.data.get('user'), 
                         id_hackaton=request.data.get('id_hackaton'), 
                         owner=request.user.pk):
        
            return JsonResponse(status=200, data={'result':'success'})
        return Response(status=404, data={'error':'Пользователь не найден'})


#получение хакатона по id
class HackatonView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        hackaton = GetHackaton().get_hackaton(request.data.get('id_hackaton'))

        if hackaton:
            return Response(status=200, data={'result':model_to_dict(hackaton)})
        return Response(status=404, data={'error':'Хакатон не найден'})
    

class HackatonUrlInvite(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        try:
            team = GetTeam().get_from_owner_hack(user=request.user, 
                                             id_hackaton=request.data.get('id_hackaton')) 
            if team is None:
                raise NotFoundTeam 
               
            key = str(uuid.uuid4())
            cache.set(key, team.pk, 10800)
        
            return Response(status=200, data={'result':'http://127.0.0.1:8000/api/v1/hackaton/invite_url/?team=' + key})
        except NotFoundTeam:
            return Response(status=404, data={'error':'Команда не найдена'})
    
    def get(self, request):
        try:
            token = request.GET.get('team')

            id_team =  cache.get(token)
            if id_team is None:
                raise NotFoundInvite

            team = GetTeam().get_team(id_team)
            if team is None:
                raise NotFoundTeam
            
            user_hack = GetHackatonUser().get_from_user_hack(user=request.user.pk, id_hackaton=team.hackaton.pk)
            if user_hack is None:
                raise NotFoundHackatonUser
            
            if len(GetUserTeam().get_list_team(id_team)) >= 5:
                raise TeamIsFull
            
            DeleteUserTeam().leave_from_team(user=request.user.pk, id_hackaton=team.hackaton.pk)
            serializer = UserTeamSerializer(data={'user': user_hack.pk, 'team':team.pk, 'is_invited':False})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=200, data={'result':'success'})
        
        except NotFoundTeam:
            return Response(status=404, data={'error':'Команда не найдена'})
        except NotFoundInvite:
            return Response(status=404, data={'error':'Приглашение в команду устарело'})
        except TeamIsFull:
            return Response(status=405, data={'error':'Команда переполнена'})
        except NotFoundHackatonUser:
            return Response(status=200, data={'error':'Вы не зарегистрированы на хакатоне'})
