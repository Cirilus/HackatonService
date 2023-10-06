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
        if User_Team.objects.get(user=Hackaton_User.objects.get(user=request.user)):
            queryset = User_Team.objects.filter(team=User_Team.objects.get(
                                                    user=Hackaton_User.objects.get(
                                                        user=request.user)).pk).only('user')
            
            serializer_class = ListTeamSerializer(queryset, many=True)

            data = {
                'team': serializer_class.data
            }
        else:
            data = {
                'team': 'error'
            }
        
        return Response({'get':data})

    


