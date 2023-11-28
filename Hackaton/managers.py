from .models import Hackaton, Hackaton_User, Team, User_Team, JoinRequest
from .exceptions import NotFoundHackaton, NotFoundHackatonUser, NotFoundInvite, NotFoundTeam, NotFoundUserTeam

class ManagerHackaton():
    def get_hackaton(self, id_hackaton):
        hackaton = Hackaton.objects.filter(pk=id_hackaton).first()
        return hackaton


class ManagerHackatonUser():
    def get_hackaton_user(self, user, id_hackaton):
        hackaton_user = Hackaton_User.objects.filter(user=user, hackaton=id_hackaton).first()
        return hackaton_user


class ManagerTeam():
    def get_team_from_pk(self, id_team):
        team = Team.objects.filter(pk=id_team).select_related('hackaton').first()
        return team
    
    def get_team_from_owner(self, id_owner):
        return Team.objects.filter(owner=id_owner).first()
    
    def delete_team(self, id_team):
        User_Team.objects.filter(team=id_team).delete()
        Team.objects.filter(pk=id_team).first().delete()


class ManagerUserTeam():
    def check_team(self, user, id_hackaton, id_team=None):
        hackaton_user = ManagerHackatonUser().get_hackaton_user(user, id_hackaton)
        if hackaton_user:
            if id_team:
                user_team = User_Team.objects.filter(user=hackaton_user, team=id_team, is_invited=True).first()
                return user_team
            user_team = User_Team.objects.filter(user=hackaton_user, is_invited=False).select_related('team').first()
            return user_team
        raise NotFoundHackatonUser('Не выполнена регистрация на хакатон')

    def get_active_invite(self, user, id_team):
        team = ManagerTeam().get_team_from_pk(id_team)
        if team:
            return ManagerUserTeam().check_team(user=user, id_hackaton=team.hackaton, id_team=id_team)
        return None
    
    def get_list_active_invites(self, user, id_hackaton):
        hackaton_user = ManagerHackatonUser().get_hackaton_user(user, id_hackaton)
        if hackaton_user:
            user_team = User_Team.objects.filter(user=hackaton_user, is_invited=True)
            return user_team
        return None
    
    def get_user_team(self, user, id_hackaton):
        return ManagerUserTeam().check_team(user=user, id_hackaton=id_hackaton)
    
    def get_list_team(self, id_team):
        user_team = User_Team.objects.filter(team=id_team, is_invited=False).select_related('user')
        return user_team
    
    def get_new_owner(self, id_team):
        list = ManagerUserTeam().get_list_team(id_team)

        if len(list) == 0:
            ManagerTeam().delete_team(id_team)
        else:
            team = ManagerTeam().get_team_from_pk(id_team)
            team.owner = list[0].user
            team.save()
    
    def delete_user_team(self, id_user_team):
        User_Team.objects.filter(pk=id_user_team).first().delete()
    
    def delete_old_user_team(self, user, id_hackaton):
        user_team = ManagerUserTeam().check_team(user=user, id_hackaton=id_hackaton)
        if user_team:
            team = user_team.team
            ManagerUserTeam().delete_user_team(id_user_team=user_team.pk)

            if team.owner == user_team.user:
                ManagerUserTeam().get_new_owner(id_team=user_team.team.pk)

class ManagerJoinRequest():
    def get_request(self, pk):
        return JoinRequest.objects.filter(pk=pk).first()
    
    def get_list_requests(self, id_team):
        return JoinRequest.objects.filter(team=id_team)

        