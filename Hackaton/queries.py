from .models import Hackaton_User, User_Team, Team, Hackaton
from rest_framework.response import Response
from .exceptions import NotFoundHackaton, NotFoundHackatonUser, NotFoundTeam, NotFoundUserTeam, NotFoundInvite, TeamIsFull
from .managers import ManagerHackaton, ManagerHackatonUser, ManagerTeam, ManagerUserTeam


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
    def get_team(self, id_team):
        team = ManagerTeam().get_team_from_pk(id_team)
        if team:
            return team
        return Response(status=404, data={'error':'Команда не найдена'})
    
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
            user_hack = ManagerHackatonUser().get_hackaton_user(user, id_hackaton)
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
    
    def get_list_team(self, id_team):
        try:         
            list = ManagerUserTeam().get_list_team(id_team)
            if list is None:
                raise NotFoundTeam
            return list

        except NotFoundTeam:
            return Response(status=404, data={'error':'Команда не найдена'})
    
    def count_users_team(self, id_team):
        list_team = GetUserTeam().get_list_team(id_team)
        if len(list_team) >= 5:
            return Response(status=405, data={'error':'Команда переполнена'})


class DeleteUserTeam():
    def leave_from_team(self, user, id_hackaton):
        user_team = ManagerUserTeam().get_user_team(user, id_hackaton)

        if user_team:
            team = user_team.team

            if team.owner == user_team.user:
                new_owner = ManagerUserTeam().get_new_owner(user, id_hackaton)

                if new_owner:
                    team.owner = new_owner.user
                    team.save()
                else:
                    team.delete()
            
            user_team.delete()

            return True
        return False

    def kick_user(self, user, id_hackaton, owner):
        try:
            team = ManagerTeam().get_team_from_owner(owner, id_hackaton)
            if team is None:
                raise NotFoundTeam
            
            user_team = ManagerUserTeam().get_user_team(user, id_hackaton)
            if user_team is None:
                raise NotFoundUserTeam
              
            user_team.delete()
    
        except NotFoundTeam:
            return Response(status=404, data={'error':'Команда не найдена'})
        except NotFoundUserTeam:
            return Response(status=404, data={'error':'Пользователь не найден'})

