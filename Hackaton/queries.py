from .models import Hackaton_User, User_Team, Team, Hackaton


class GetHackaton():
    def get_hackaton(self, pk):
        return Hackaton.objects.filter(pk=pk).first()
    
    def list_hackaton(self):
        return Hackaton.objects.all()


class GetHackatonUser():
    def get_from_user_hack(self, user, id_hackaton):
        return Hackaton_User.objects.filter(user=user, hackaton=id_hackaton).first()


class GetTeam():
    def get_team(id_team):
        return Team.objects.filter(pk=id_team).first()
    
    def get_from_owner_hack(self, user, id_hackaton):
        owner = GetHackatonUser().get_from_user_hack(user, id_hackaton)
        if owner:
            return Team.objects.filter(owner=owner).first()
        return None
    
    def delete_team(self, team):
        team = Team.objects.filter(pk=team).first()
        if team:
            team.delete()
    

class GetUserTeam():
    def get_invited(self, team, user):
        return User_Team.objects.filter(team=team, user__user=user, is_invited=True).first()
    
    def get_from_user(self, user, id_hackaton):
        user_hack = GetHackatonUser().get_from_user_hack(user, id_hackaton)
        if user_hack:
            return User_Team.objects.filter(user=user_hack, is_invited=False).first()
        return None
    
    def get_list_team(self, team):
        return User_Team.objects.filter(team=team, is_invited=False).select_related('user')
    

class DeleteUserTeam():
    def leave_from_team(self, user, id_hackaton):
        user_team = GetUserTeam().get_from_user(user, id_hackaton)

        if not user_team is None:
            team = user_team.team

            if team.owner == user_team.user:
                new_owner = GetUserTeam().get_from_user(user=user, id_hackaton=id_hackaton)

                if new_owner:
                    team.owner = new_owner.user
                    team.save()
                else:
                    team.delete()
            
            user_team.delete()

            return True
        
        return False

    def kick_user(self, user, id_hackaton, owner):
        team = GetTeam().get_from_owner_hack(owner, id_hackaton)

        if team:
            hack_user = GetUserTeam().get_from_user(user, id_hackaton)
            
            if hack_user:
                hack_user.delete()
                return True
            
        return False

