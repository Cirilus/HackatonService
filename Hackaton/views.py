from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import HackatonUserSerializer, ListTeamSerializer, TeamSerializer, HackatonSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import User_Team, Team, Hackaton_User, Hackaton
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from .queries import get_hackaton_user, get_user_team, get_list_team, get_team, delete_user_team, get_hackaton


#регистрация пользователя на хакатон
class HackatonUserView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        request.data['user'] = request.user.pk
        serializer = HackatonUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse({'result':'success'})


#получение списка своей команды по id хакатона
class MyTeamListView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        data = {}
        user = get_user_team(user=request.user, id_hackaton=request.data.get('id_hackaton'))

        if user: 
            queryset = get_list_team(user.team)
            serializer_class = ListTeamSerializer(queryset, many=True)

            data['result'] = 'success'
            data['team'] = serializer_class.data
        else:
            data['result'] = 'error'

        return JsonResponse(data)


#Приглашение в команду
class InviteTeamView(APIView):
    permission_classes = [IsAuthenticated,]
    
    #дать инвайт
    def post(self, request):
        data = {}

        user = get_hackaton_user(pk=request.data.get('user'))
        team = get_team(request.user, request.data.get('id_hackaton'))

        if team is None:
            data['result'] = 'error'
        else:
            serializer = TeamSerializer(data={'user': user.pk, 'team':team.pk})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            data['result'] = 'success'

        return JsonResponse(data)
    
    #принять инвайт
    def put(self, request):
        data = {}

        user_team = get_user_team(team=request.data.get('team'), user=request.user)

        if user_team is None:
            data['result'] = 'error'
        else:
            delete_user_team(user=request.user, id_hackaton=user_team.user.hackaton)

            user_team.is_invited = False
            user_team.save()

            data['result'] = 'success'

        return JsonResponse(data)
    

    #Выйти из команды
    def delete(self, request):
        data = {}

        if delete_user_team(user=request.user, 
                            id_hackaton=request.data.get('id_hackaton')):
            data['result'] = 'success'
        else:
            data['result'] = 'error'

        return JsonResponse(data)


class KickUserView(APIView):
    permission_classes = [IsAuthenticated,]

    #Удалить юзера из команды (id_user, id_hackaton)
    def delete(self, request):
        delete_user_team(user=request.data.get('id_user'), 
                         id_hackaton=request.data.get('id_hackaton'), 
                         owner=request.user)
        
        return JsonResponse({'result':'success'})


#получение хакатона по id
class HackatonView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        hackaton = get_hackaton(request.data.get('id_hackaton'))

        if hackaton:
            data['result'] = 'success'
            data['hackaton'] = model_to_dict(hackaton)
        else:
            data['result'] = 'error'

        return JsonResponse(data)