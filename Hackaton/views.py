from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import HackatonUserSerializer, ListTeamSerializer
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
    
    def post(self, request):
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
                    'answer':'ok',
                    'team': serializer_class.data
                }
                
            else:
                data = {
                'answer': 'not on team'
            }
                
        else:
            data = {
                'answer': 'not registered'
            }
        
        return Response({'get':data})

    


