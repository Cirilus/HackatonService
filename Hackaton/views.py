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
from .queries import GetHackaton, GetHackatonUser, GetTeam, GetUserTeam, DeleteUserTeam


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
        user = GetUserTeam().get_from_user(user=request.user.pk, id_hackaton=request.data.get('id_hackaton'))

        if user: 
            queryset = GetTeam().get_list_team(user.team.pk)
            serializer_class = ListTeamSerializer(queryset, many=True)

            data['result'] = 'success'
            data['data'] = serializer_class.data
        else:
            data['result'] = 'error'
            data['data'] = '404'

        return JsonResponse(data)


#Приглашение в команду
class InviteTeamView(APIView):
    permission_classes = [IsAuthenticated,]
    
    #дать инвайт
    def post(self, request):
        data = {}

        user = GetHackatonUser().get_from_user_hack(request.data.get('user'), request.data.get('id_hackaton'))
        team = GetTeam().get_from_owner_hack(request.user.pk, request.data.get('id_hackaton'))
        print(team.owner)
        if team is None:
            data['result'] = 'error'
            data['data'] = '404'
        else:
            serializer = TeamSerializer(data={'user': user.pk, 'team':team.pk})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            data['result'] = 'success'

        return JsonResponse(data)
    
    #принять инвайт
    def put(self, request):
        data = {}

        user_team = GetUserTeam().get_invited(team=request.data.get('team'), user=request.user.pk)

        if user_team is None:
            data['result'] = 'error'
            data['data'] = '404'
        else:
            DeleteUserTeam.leave_from_team(user=request.user.pk, id_hackaton=user_team.user.hackaton.pk)

            user_team.is_invited = False
            user_team.save()

            data['result'] = 'success'

        return JsonResponse(data)
    

    #Выйти из команды
    def delete(self, request):
        data = {}

        if DeleteUserTeam().leave_from_team(request.user, 
                            request.data.get('id_hackaton')):
            data['result'] = 'success'
        else:
            data['result'] = 'error'
            data['data'] = '405'

        return JsonResponse(data)


class KickUserView(APIView):
    permission_classes = [IsAuthenticated,]

    #Удалить юзера из команды
    def delete(self, request):
        if DeleteUserTeam().kick_user(user=request.data.get('user'), 
                         id_hackaton=request.data.get('id_hackaton'), 
                         owner=request.user.pk):
        
            return JsonResponse({'result':'success'})
        return JsonResponse({'result':'error', 'data':'405'})


#получение хакатона по id
class HackatonView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        hackaton = GetHackaton().get_hackaton(request.data.get('id_hackaton'))

        if hackaton:
            data['result'] = 'success'
            data['data'] = model_to_dict(hackaton)
        else:
            data['result'] = 'error'
            data['data'] = '405'

        return JsonResponse(data)