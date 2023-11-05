from .models import Hackaton_User, User_Team, Team, Hackaton
from .serializers import TeamSerializer, UserTeamSerializer, ListTeamSerializer
from rest_framework.response import Response
from rest_framework import status
from .exceptions import NotFoundHackaton, NotFoundHackatonUser, NotFoundTeam, NotFoundUserTeam, NotFoundInvite, TeamIsFull
from .managers import ManagerHackaton, ManagerHackatonUser, ManagerTeam, ManagerUserTeam
import uuid
from django.core.cache import cache

class GetHackaton():
    def get_hackaton(self, pk):
        hackaton = ManagerHackaton().get_hackaton(pk)
        if hackaton is None:
            return Response(status=404, data={'error':'Хакатон не найден'})
        return hackaton
    
    def list_hackaton(self):
        return Hackaton.objects.all()


class GetHackatonUser():
    def get_from_user_hack(self, user, id_hackaton):
        user_hack = ManagerHackatonUser().get_hackaton_user(user, id_hackaton)
        if user_hack:
            return user_hack
        return Response(status=404, data={'error':'Вы не зарегистрированы на хакатоне'})
    
    def get_user_hack_for_invite(self, user, id_hackaton):
        user_hack = ManagerHackatonUser().get_hackaton_user(user, id_hackaton)
        if user_hack:
            return user_hack
        return Response(status=404, data={'error':'Пользователь не зарегистрирован на хакатоне'})

class GetTeam():
    def get_team(self, data):
        try:
            queryset = ManagerTeam().get_team_from_pk(data.get('team'))
            if queryset is None:
                raise NotFoundTeam('команда не найдена')
            
            serializer = TeamSerializer(queryset)
            return Response(status=200, data={'result':serializer.data})
        
        except NotFoundTeam as e:
            return Response(status=404, data={'error':str(e)})
    
    def get_my_team(self, user, data):
        try:
            hackaton = ManagerHackaton().get_hackaton(id_hackaton=data.get('id_hackaton'))
            if hackaton is None:
                raise NotFoundHackaton('Хакатон не найден')

            user_team = ManagerUserTeam().get_user_team(user=user, id_hackaton=hackaton.pk)
            if user_team is None:
                raise NotFoundUserTeam('Вы не состоите в команде')

            queryset = ManagerUserTeam().get_list_team(id_team=user_team.team)
            serializer_class = ListTeamSerializer(queryset, many=True)
            return Response(status=200, data={'result':serializer_class.data})

        except NotFoundHackaton as e:
            return Response(status=404, data={'error':str(e)})
        except NotFoundUserTeam as e:
            return Response(status=404, data={'error':str(e)})
        except NotFoundHackatonUser as e:
            return Response(status=404, data={'error':str(e)})
        
    def create_team(self, user, data):
        try:
            hackaton = ManagerHackaton().get_hackaton(id_hackaton=data['id_hackaton'])
            if hackaton is None:
                raise NotFoundHackaton('Хакатон не найден')
            
            ManagerUserTeam().delete_old_user_team(user=user, id_hackaton=hackaton)
            
            hackaton_user = ManagerHackatonUser().get_hackaton_user(user=user, id_hackaton=hackaton.pk)
            data['owner'] = hackaton_user.pk
            data['hackaton'] = hackaton.pk
            
            serializer = TeamSerializer(data=data)  
            serializer.is_valid(raise_exception=True) 
            serializer.save()

            data['team'] = serializer.data['id']
            data['user'] = hackaton_user.pk
            data['is_invited'] = False

            serializer = UserTeamSerializer(data=data)
            serializer.is_valid(raise_exception=True) 
            serializer.save()
            return Response(status=200, data={'result':'success'})

        except NotFoundHackaton as e:
            return Response(status=404, data={'error':str(e)})
        except NotFoundHackatonUser:
            return Response(status=404, data={'error':'Вы не зарегистрированы на данный хакатон'})
        
    def get_from_owner_hack(self, user, id_hackaton):
        try:
            owner = ManagerHackatonUser().get_hackaton_user(user, id_hackaton)
            if owner is None:
                raise NotFoundHackatonUser
            
            team = ManagerTeam().get_team_from_owner(user, id_hackaton)
            if team is None:
                raise NotFoundTeam
            
            return team

        except NotFoundTeam:
            return Response(status=404, data={'error':'Вы не являетесь создателем команды на данном хакатоне'})
        except NotFoundHackatonUser:
            return Response(status=404, data={'error':'Вы не зарегистрированы на хакатоне'})
    
    def delete_team(self, team):
        team = Team.objects.filter(pk=team).first()
        if team:
            team.delete()
    

class GetUserTeam():
    def get_invited(self, team, user):
        user_team = ManagerUserTeam().get_active_invite(user, team)
        if user_team:
            return user_team
        return Response(status=404, data={'error':'Приглашение не найдено'})
    
    def get_from_user(self, user, id_hackaton):
        try:
            user_hack = ManagerHackatonUser().get_hackaton_user(user=user, id_hackaton=id_hackaton)
            if user_hack is None:
                raise NotFoundHackatonUser
            
            user_team = User_Team.objects.filter(user=user_hack, is_invited=False).first()
            if user_team is None:
                raise NotFoundUserTeam
            return user_team
        
        except NotFoundUserTeam:
            return Response(status=404, data={'error':'Вы не состоите в команде'})
        except NotFoundHackatonUser:
            return Response(status=404, data={'error':'Вы не зарегистрированы на хакатон'})
    
    def create_invite(self, user, data):
        try:
            owner = ManagerHackatonUser().get_hackaton_user(user=user, id_hackaton=data.get('id_hackaton'))
            if owner is None:
                raise NotFoundHackatonUser('Вы не зарегистрированы на данном хакатоне')

            team = ManagerTeam().get_team_from_owner(id_owner=owner)
            if team is None:
                raise NotFoundTeam('Вы не создатель команды')
            
            user_hackaton = ManagerHackatonUser().get_hackaton_user(user=data.get('user'), id_hackaton=data.get('id_hackaton'))
            if user_hackaton is None:
                return Response(status=404, data={'error':'Пользователь не найден'})

            data['user'] = user_hackaton.pk
            data['team'] = team.pk
            data['is_invited'] = False

            serializer = UserTeamSerializer(data=data)
            serializer.is_valid(raise_exception=True) 
            serializer.save()
            return Response(status=200, data={'result':'success'})
        
        except NotFoundHackatonUser as e:
            return Response(status=404, data={'error':str(e)})
        except NotFoundTeam as e:
            return Response(status=404, data={'error':str(e)})

    def accept_invite(self, user, data):
        try:
            user_team = ManagerUserTeam().get_active_invite(user=user, id_team=data.get('team'))
            if user_team is None:
                raise NotFoundInvite('Приглашение не найдено')
            
            list_team = ManagerUserTeam().get_list_team(id_team=data.get('team'))
            if len(list_team) >= 5:
                ManagerUserTeam().delete_user_team(user_team)
                raise TeamIsFull('Команда переполнена')
            
            ManagerUserTeam().delete_old_user_team(user=user, id_hackaton=user_team.team.hackaton)

            user_team.is_invited = False
            user_team.save()
            return Response(status=200, data={'result':'success'})

        except NotFoundInvite as e:
            return Response(status=404, data={'error':str(e)})
        except TeamIsFull as e:
            return Response(status=405, data={'error':str(e)})
        
    def create_invite_url(self, user, data):
        try:
            hackaton_user = ManagerHackatonUser().get_hackaton_user(user=user, id_hackaton=data.get('id_hackaton'))
            if hackaton_user is None:
                raise NotFoundHackatonUser('Вы не зарегистрированы на хакатон')
            
            team = ManagerTeam().get_team_from_owner(id_owner=hackaton_user)
            if team is None:
                raise NotFoundTeam('Вы не создатель команды')
            
            key = str(uuid.uuid4())
            cache.set(key, team.pk, 10800)

            return Response(status=200, data={'result':'http://127.0.0.1:8000/api/v1/hackaton/invite_url/?team=' + key})
        
        except NotFoundHackatonUser as e:
            return Response(status=405, data={'error':str(e)})
        except NotFoundTeam as e:
            return Response(status=405, data={'error':str(e)})

    def accept_url_invite(self, user, key):
        id_team = cache.get(key)
        if id_team is None:
            return Response(status=404, data={'error':'Приглашение в команду устарело'})
        return GetUserTeam().accept_invite(user=user, data={'team':id_team})

    def count_users_team(self, id_team):
        list_team = GetUserTeam().get_list_team(id_team)
        if len(list_team) >= 5:
            return Response(status=405, data={'error':'Команда переполнена'})


class DeleteUserTeam():
    def leave_from_team(self, user, id_hackaton):
        user_team = ManagerUserTeam().get_user_team(user, id_hackaton)

        if user_team:
            team = user_team.team
            hack_user = user_team.user

            ManagerUserTeam().delete_user_team(id_user_team=user_team.pk)

            if team.owner == hack_user:
                ManagerUserTeam().get_new_owner(team.pk)
            return True
        return False

    def kick_user(self, user, id_hackaton, owner):
        try:
            hackaton_user = ManagerHackatonUser().get_hackaton_user(user=owner, id_hackaton=id_hackaton)
            if hackaton_user is None:
                raise NotFoundHackatonUser('Вы не зарегистрированы на хакатон')
            
            team = ManagerTeam().get_team_from_owner(id_owner=hackaton_user)
            if team is None:
                raise NotFoundTeam('Команда не найдена')
            
            user_team = ManagerUserTeam().get_user_team(user, id_hackaton)
            if user_team is None:
                raise NotFoundUserTeam('Пользователь не найден')
              
            ManagerUserTeam().delete_user_team(user_team)
            return Response(status=200, data={'result':'success'})
        
        except NotFoundTeam as e:
            return Response(status=404, data={'error':str(e)})
        except NotFoundUserTeam as e:
            return Response(status=404, data={'error':str(e)})
        except NotFoundHackatonUser as e:
            return Response(status=404, data={'error':str(e)})


