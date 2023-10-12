from .models import Hackaton_User, User_Team, Team, Hackaton

def get_hackaton_user(pk=None, user=None, id_hackaton=None):
    if pk:
        return Hackaton_User.objects.filter(pk=pk).first()
    else:
        return Hackaton_User.objects.filter(user=user, hackaton=id_hackaton).first()


def get_user_team(team=None, user=None, id_hackaton=None):
    if team:
        return User_Team.objects.filter(team=team, user__user=user, is_invited=True).first()
    else:
        hackaton_user = get_hackaton_user(user=user, id_hackaton=id_hackaton)
        return User_Team.objects.filter(user=hackaton_user, is_invited=False).first()


def get_list_team(team):
    return User_Team.objects.filter(team=team, is_invited=False).select_related('user')


def get_team(owner, id_hackaton):
    user = get_hackaton_user(user=owner, id_hackaton=id_hackaton)
    return Team.objects.filter(owner=user).first()


def delete_user_team(user, id_hackaton, owner=None):
    if owner:
        team = Team.objects.filter(owner=get_hackaton_user(user=owner, id_hackaton=id_hackaton)).first()
        User_Team.objects.filter(team=team, user__user=user).first().delete()

    else:
        user_hackaton = get_hackaton_user(user=user, id_hackaton=id_hackaton)
        user_team = User_Team.objects.filter(user=user_hackaton, is_invited=False).first()

        if user_team:
            user_team.delete()

            return True


def get_hackaton(id_hackaton):
    return Hackaton.objects.filter(pk=id_hackaton).first()