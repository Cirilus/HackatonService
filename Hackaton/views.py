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
from rest_framework.decorators import action, permission_classes, api_view
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
    #получить по id
    def get(self, request):
        response = GetTeam().get_team(request.data)
        return response

    #создать команду
    def post(self, request):
        response = GetTeam().create_team(user=request.user, data=request.data)
        return response


#получение списка своей команды по id хакатона
class MyTeamListView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        response = GetTeam().get_my_team(user=request.user.pk, data=request.data)
        return response
        

#Приглашение в команду
class InviteTeamView(APIView):
    permission_classes = [IsAuthenticated,]
    
    #дать инвайт
    def post(self, request):
        response = GetUserTeam().create_invite(user=request.user, data=request.data)
        return response
    
    #принять инвайт 
    def update(self, request):
        response = GetUserTeam().accept_invite(user=request.user, data=request.data)
        return response
    
    #Выйти из команды
    def put(self, request):
        DeleteUserTeam().leave_from_team(request.user.pk, 
                            request.data.get('id_hackaton'))
        return Response(status=200, data={'result':'success'})


class KickUserView(APIView):
    permission_classes = [IsAuthenticated,]

    #Удалить юзера из команды
    def delete(self, request):
        response = DeleteUserTeam().kick_user(user=request.data.get('user'), 
                         id_hackaton=request.data.get('id_hackaton'), 
                         owner=request.user.pk)  
        return response   


#получение хакатонов по заданным фильтрам
class HackatonListView(generics.GenericAPIView, 
                      mixins.CreateModelMixin, 
                      mixins.ListModelMixin):
    permission_classes = [AllowAny,]
    serializer_class = HackatonSerializer

    def get_queryset(self):
        queryset = Hackaton.objects.all()
        filter = {}
        for i in self.request.data.keys():
            filter[i] = self.request.data[i]
        return queryset.filter(**filter)
    

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class HackatonCreateView(generics.GenericAPIView, 
                         mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated,]
    serializer_class = HackatonSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class HackatonUrlInvite(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        response = GetUserTeam().create_invite_url(user=request.user, data=request.data)
        return response
    
    def get(self, request):
        response = GetUserTeam().accept_url_invite(user=request.user, key=request.GET.get('team'))
        return response
