from .models import Hackaton, Hackaton_User, Team, User_Team


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
    
    def get_team_from_owner(self, user, id_hackaton):
        hackaton_user = ManagerHackatonUser().get_hackaton_user(user, id_hackaton)
        if hackaton_user:
            team = Team.objects.filter(owner=hackaton_user).first()
            return team
        return None


class ManagerUserTeam():
    def check_team(self, user, id_hackaton, id_team=None):
        hackaton_user = ManagerHackatonUser().get_hackaton_user(user, id_hackaton)
        if hackaton_user:
            if id_team:
                user_team = User_Team.objects.filter(user=hackaton_user, team=id_team, is_invited=True).first()
                return user_team
            user_team = User_Team.objects.filter(user=hackaton_user, is_invited=False).select_related('team').first()
            return user_team
        return None

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
        return ManagerUserTeam(user=user, id_hackaton=id_hackaton)
    
    def get_list_team(self, id_team):
        team = ManagerTeam().get_team_from_pk(id_team)
        if team:
            user_team = User_Team.objects.filter(team=team, is_invited=False).select_related('user')
            return user_team
        return None
    
    def get_new_owner(self, user, id_hackaton):
        user_team = ManagerUserTeam().get_user_team(user, id_hackaton)
        if user_team is None:
            return None
        
        list = ManagerUserTeam().get_list_team(user_team.team)
        if len(list) < 2:
            return None
        return list[1]
        