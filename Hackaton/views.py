from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import HackatonUserSerializer, ListTeamSerializer, InviteTeamSErializer
from rest_framework.response import Response
from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated


#регистрация пользователя на хакатон
class HackatonUserView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        serializer = HackatonUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'status':'ok'})


#получение списка своей команды по id хакатона
class MyTeamListView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        data = {}
        if Hackaton_User.objects.filter(hackaton=request.data.get('id'), 
                                        user=request.user).exists():
            
            if User_Team.objects.filter(user=Hackaton_User.objects.filter(
                                            hackaton=request.data.get('id'), 
                                            user=request.user).exists()):
                
                queryset = User_Team.objects.filter(team=User_Team.objects.get(
                                                        user=Hackaton_User.objects.get(
                                                            hackaton=request.data.get('id'), 
                                                            user=request.user)).pk).only('user')
            
                serializer_class = ListTeamSerializer(queryset, many=True)

                data = {
                    'status':'ok',
                    'team': serializer_class.data
                }

            else:
                data['status'] = 'not on team'
                
        else:
            data['status'] = 'not registered on hackaton'
        
        return Response({'get':data})

#Приглашение в команду
class InviteTeamView(APIView):
    permission_classes = [IsAuthenticated,]
    
    #дать инвайт
    def post(self, request):
        data = {}

        if Hackaton_User.objects.filter(
                                        user=request.user, 
                                        hackaton=request.data.get('id')
                                        ).exists() and Hackaton_User.objects.filter(
                                        pk=request.data.get('user')
                                        ).exists():

            if Team.objects.filter(owner=Hackaton_User.objects.get(
                                        user=request.user, 
                                        hackaton=request.data.get('id')
                                        )).exists():

                if not User_Team.objects.filter(user=Hackaton_User.objects.get(
                                        pk=request.data.get('user'))).exists():

                    serializer = InviteTeamSErializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    data['status'] = 'ok'
                else:
                    data['status'] = 'already on team'
            else:
                data['status'] = 'not the owner'
        else:
            data['status'] = 'not registered on hackaton'
        
        return Response(data)
    
    #принять инвайт
    def delete(self, request):
        data = {}

        if Team_Invite.objects.filter(pk=request.data.get('id'), 
                                      user=Hackaton_User.objects.get(
                                                        user=request.user)).exists():
            
            team = Team_Invite.objects.get(pk=request.data.get('id')).team

            Team_Invite.objects.filter(user=Hackaton_User.objects.get(
                                                    user=request.user),
                                                    team__hackaton=team.hackaton
                                                    ).delete()
            User_Team.objects.create(user=Hackaton_User.objects.get(user=request.user, hackaton=team.hackaton), team=team)

            data['status'] = 'ok'

        else:
            data['status'] = 'not found invite'

        return Response(data)


