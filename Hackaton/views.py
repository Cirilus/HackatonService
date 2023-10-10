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


#регистрация пользователя на хакатон
class HackatonUserView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        serializer = HackatonUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse({'status':'ok'})


#получение списка своей команды по id хакатона
class MyTeamListView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        data = {}
        
        try:
            user = User_Team.objects.get(user=Hackaton_User.objects.get(
                                            hackaton=request.data.get('id_hackaton'), 
                                            user=request.user), is_invited=False)
        except:
            data['status'] = 'not registered on hackaton'

        else:   
            queryset = User_Team.objects.filter(team=user.team,is_invited=False).select_related('user')
            serializer_class = ListTeamSerializer(queryset, many=True)

            data = {
                'status':'ok',
                'team': serializer_class.data
            }
        
        return JsonResponse({'get':data})

#Приглашение в команду
class InviteTeamView(APIView):
    permission_classes = [IsAuthenticated,]
    
    #дать инвайт
    def post(self, request):
        data = {}

        try:
            user = Hackaton_User.objects.get(pk=request.data.get('user'))
            team = Team.objects.get(owner=Hackaton_User.objects.get(user=request.user,
                                                                     hackaton=request.data.get('id_hackaton')))
        except:
            data['status'] = 'not found user'

        else:
            serializer = TeamSerializer(data={'user': user.pk, 'team':team.pk})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            data['status'] = 'ok'

        return JsonResponse(data)
    
    #принять инвайт
    def put(self, request):
        data = {}

        try:
            user_team = User_Team.objects.get(pk=request.data.get('id_invite'))
            user = Hackaton_User.objects.get(user=request.user, hackaton=user_team.team.hackaton)
        except:
            data['status'] = 'not found invite'
        
        else:
            try:
                User_Team.objects.get(user=user, team__hackaton=user_team.team.hackaton, is_invited=False).delete()
            except:
                pass

            user_team.is_invited = False
            user_team.save()

            data['status'] = 'ok'

        return JsonResponse(data)
    

    #Выйти из команды
    def delete(self, request):
        data = {}

        try:
            User_Team.objects.get(user=Hackaton_User.objects.get(
                                                                hackaton=request.data.get('id_hackaton'), 
                                                                user=request.user),
                                                                is_invited=False
                                                                ).delete()
            data['status'] = 'ok'
        except:
            data['status'] = 'not found'

        return JsonResponse(data)


class KickUserView(APIView):
    permission_classes = [IsAuthenticated,]
    #Удалить юзера из команды (id_hackaton_user, id_hackaton)
    def delete(self, request):
        data = {}
        try:
            team = Team.objects.get(owner=Hackaton_User.objects.get(user=request.user, 
                                                                    hackaton=request.data.get('id_hackaton')))
            User_Team.objects.get(team=team, user=request.data.get('id_hackaton_user')).delete()
            data['status'] = 'success'
            
        except:
            data['status'] = 'error'
        
        return JsonResponse(data)


#получение хакатона по id
class HackatonView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        hackaton = Hackaton.objects.get(pk=request.data.get('id_hackaton'))
        return JsonResponse(model_to_dict(hackaton))