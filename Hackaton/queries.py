from .models import Hackaton_User, User_Team, Team, Hackaton
from .serializers import TeamSerializer, UserTeamSerializer, ListTeamSerializer, JoinRequestSerializer
from rest_framework.response import Response
from rest_framework import status
from .exceptions import NotFoundHackaton, NotFoundHackatonUser, NotFoundTeam, NotFoundUserTeam, NotFoundInvite, TeamIsFull, NotFoundJoinRequest
from .managers import ManagerHackaton, ManagerHackatonUser, ManagerTeam, ManagerUserTeam, ManagerJoinRequest
import uuid
from django.core.cache import cache
from .errors import DoesNotFoundTeam, UserDoesNotRegistrationInHackaton, YouDontRegistrationInHackaton, DontFoundHackaton, YouAreNotCreatorTeam, InviteDontFound, YouAreNotInTeam, UserDoesNotFound, FullTeam, OldInvite, DoesNotFoundRequest

class GetHackaton():
    def get_hackaton(self, pk):
        hackaton = ManagerHackaton().get_hackaton(pk)
        if hackaton is None:
            return Response(status=404, data={'error':DontFoundHackaton().value})
        return hackaton
    
    def list_hackaton(self):
        return Hackaton.objects.all()


class GetHackatonUser():
    def get_from_user_hack(self, user, id_hackaton):
        user_hack = ManagerHackatonUser().get_hackaton_user(user, id_hackaton)
        if user_hack:
            return user_hack
        return Response(status=404, data={'error':YouDontRegistrationInHackaton().value})
    
    def get_user_hack_for_invite(self, user, id_hackaton):
        user_hack = ManagerHackatonUser().get_hackaton_user(user, id_hackaton)
        if user_hack:
            return user_hack
        return Response(status=404, data={'error':UserDoesNotRegistrationInHackaton().value})

class GetTeam():
    def get_team(self, data):
        try:
            queryset = ManagerTeam().get_team_from_pk(data.get('team'))
            if queryset is None:
                raise NotFoundTeam(DoesNotFoundTeam().value)
            
            serializer1 = TeamSerializer(queryset)
            queryset = ManagerUserTeam().get_list_team(id_team=data.get('team'))
            serializer2 = ListTeamSerializer(queryset, many=True)
            return Response(status=200, data={'result':{'list_team':serializer2.data, 'team':serializer1.data}})
        
        except NotFoundTeam as e:
            return Response(status=404, data={'error':str(e)})
    
    def get_my_team(self, user, data):
        try:
            hackaton = ManagerHackaton().get_hackaton(id_hackaton=data.get('id_hackaton'))
            if hackaton is None:
                raise NotFoundHackaton(DontFoundHackaton().value)

            user_team = ManagerUserTeam().get_user_team(user=user, id_hackaton=hackaton.pk)
            if user_team is None:
                raise NotFoundUserTeam('Вы не состоите в команде')

            queryset = ManagerUserTeam().get_list_team(id_team=user_team.team)
            serializer1 = ListTeamSerializer(queryset, many=True)
            queryset = ManagerTeam().get_team_from_pk(user_team.team.pk)
            serializer2 = TeamSerializer(queryset)
            return Response(status=200, data={'result':{'team_list':serializer1.data, 'team':serializer2.data}})

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
                raise NotFoundHackaton(DontFoundHackaton().value)
            
            ManagerUserTeam().delete_old_user_team(user=user, id_hackaton=hackaton.pk)
            
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
            return Response(status=404, data={'error':YouDontRegistrationInHackaton().value})
        
    def get_from_owner_hack(self, user, id_hackaton):
        try:
            owner = ManagerHackatonUser().get_hackaton_user(user, id_hackaton)
            if owner is None:
                raise NotFoundHackatonUser('')
            
            team = ManagerTeam().get_team_from_owner(user, id_hackaton)
            if team is None:
                raise NotFoundTeam
            
            return team

        except NotFoundTeam:
            return Response(status=404, data={'error':YouAreNotCreatorTeam().value})
        except NotFoundHackatonUser:
            return Response(status=404, data={'error':YouDontRegistrationInHackaton().value})
    
    def delete_team(self, team):
        team = Team.objects.filter(pk=team).first()
        if team:
            team.delete()
    

class GetUserTeam():
    def get_invited(self, team, user):
        user_team = ManagerUserTeam().get_active_invite(user, team)
        if user_team:
            return user_team
        return Response(status=404, data={'error':InviteDontFound().value})

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
            return Response(status=404, data={'error':YouAreNotInTeam().value})
        except NotFoundHackatonUser:
            return Response(status=404, data={'error':YouDontRegistrationInHackaton().value})
    
    def create_invite(self, user, data):
        try:
            owner = ManagerHackatonUser().get_hackaton_user(user=user, id_hackaton=data.get('id_hackaton'))
            if owner is None:
                raise NotFoundHackatonUser(YouDontRegistrationInHackaton().value)

            team = ManagerTeam().get_team_from_owner(id_owner=owner)
            if team is None:
                raise NotFoundTeam(YouAreNotCreatorTeam().value)
            
            user_hackaton = ManagerHackatonUser().get_hackaton_user(user=data.get('user'), id_hackaton=data.get('id_hackaton'))
            if user_hackaton is None:
                return Response(status=404, data={'error':UserDoesNotFound().value})

            data['user'] = user_hackaton.pk
            data['team'] = team.pk
            data['is_invited'] = True

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
                raise NotFoundInvite(InviteDontFound().value)
            
            list_team = ManagerUserTeam().get_list_team(id_team=data.get('team'))
            if len(list_team) >= 5:
                ManagerUserTeam().delete_user_team(user_team)
                raise TeamIsFull(FullTeam().value)
            
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
                raise NotFoundHackatonUser(YouDontRegistrationInHackaton().value)
            
            team = ManagerTeam().get_team_from_owner(id_owner=hackaton_user)
            if team is None:
                raise NotFoundTeam(YouAreNotCreatorTeam().value)
            
            key = str(uuid.uuid4())
            cache.set(key, team.pk, 10800)

            return Response(status=200, data={'result':'http://127.0.0.1:8000/api/v1/hackaton/invite_url/?team=' + key})
        
        except NotFoundHackatonUser as e:
            return Response(status=405, data={'error':str(e)})
        except NotFoundTeam as e:
            return Response(status=405, data={'error':str(e)})

    def accept_url_invite(self, user, key):
        try:
            id_team = cache.get(key)
            if id_team is None:
                return Response(status=404, data={'error':OldInvite().value})
            list_team = ManagerUserTeam().get_list_team(id_team=id_team)
            if len(list_team) >= 5:
                raise TeamIsFull(FullTeam().value)
            
            team = ManagerTeam().get_team_from_pk(id_team=id_team)
            user_hackaton = ManagerHackatonUser().get_hackaton_user(user=user, id_hackaton=team.hackaton)
            ManagerUserTeam().delete_old_user_team(user=user, id_hackaton=team.hackaton)

            data = {
                'user': user_hackaton.pk,
                'team': team.pk,
                'is_invited': False
            }

            serializer = UserTeamSerializer(data=data)
            serializer.is_valid(raise_exception=True) 
            serializer.save()
            return Response(status=200, data={'result':'success'})

        except NotFoundInvite as e:
            return Response(status=404, data={'error':str(e)})
        except TeamIsFull as e:
            return Response(status=405, data={'error':str(e)})
        

    def count_users_team(self, id_team):
        list_team = GetUserTeam().get_list_team(id_team)
        if len(list_team) >= 5:
            return Response(status=405, data={'error':FullTeam().value})


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
                raise NotFoundHackatonUser(YouDontRegistrationInHackaton().value)
            
            team = ManagerTeam().get_team_from_owner(id_owner=hackaton_user)
            if team is None:
                raise NotFoundTeam(DoesNotFoundTeam().value)
            
            user_team = ManagerUserTeam().get_user_team(user, id_hackaton)
            if user_team is None:
                raise NotFoundUserTeam(UserDoesNotFound().value)
            
            ManagerUserTeam().delete_user_team(id_user_team=user_team.pk)
            return Response(status=200, data={'result':'success'})
        
        except NotFoundTeam as e:
            return Response(status=404, data={'error':str(e)})
        except NotFoundUserTeam as e:
            return Response(status=404, data={'error':str(e)})
        except NotFoundHackatonUser as e:
            return Response(status=404, data={'error':str(e)})


class QueriesJoinRequest():
    def filter_requests(self, user, id_hackaton):
        hack_user = ManagerHackatonUser().get_hackaton_user(user=user, id_hackaton=id_hackaton)
        team = ManagerTeam().get_team_from_owner(id_owner=hack_user.pk)
        requests = ManagerJoinRequest().get_list_requests(id_team=team.pk).filter(status='pending')
        return requests

    def create_join_request(self, user, team):
        try:
            data = {}
            team = ManagerTeam().get_team_from_pk(id_team=team)
            if team is None:
                raise NotFoundTeam(FullTeam().value)
            data['team'] = team.pk

            hack_user = ManagerHackatonUser().get_hackaton_user(user=user, id_hackaton=team.hackaton)
            if hack_user is None:
                raise NotFoundHackatonUser(YouDontRegistrationInHackaton().value)
            data['user'] = hack_user.pk

            invite = ManagerUserTeam().get_active_invite(user=user, id_team=team.pk)
            if invite is None:
                serializer = JoinRequestSerializer(data=data)
                serializer.is_valid(raise_exception=True) 
                serializer.save()
                return Response(status=200, data={'result':'success'})
            
            return GetUserTeam().accept_invite(user=user, data={'team':team.pk})
        
        except NotFoundTeam as e:
            return Response(status=404, data={'error':str(e)})
        except NotFoundHackatonUser as e:
            return Response(status=404, data={'error':str(e)})
    
    def answer_request(self, user, id_join, answer):
        try:
            statuses = {'True':'accept',
                        'False':'decline'}
            join_request = ManagerJoinRequest().get_request(pk=id_join)
            if join_request is None:
                raise NotFoundJoinRequest(DoesNotFoundRequest().value)
            
            owner = ManagerHackatonUser().get_hackaton_user(user=user, id_hackaton=join_request.team.hackaton.pk)
            if owner is None or join_request.team.owner.pk != owner.pk:
                raise NotFoundHackatonUser()
            
            join_request.status = statuses[answer]
            join_request.save()

            list_team = ManagerUserTeam().get_list_team(id_team=join_request.team)
            if join_request.status == 'accept' and len(list_team) < 5:
                serializer_user_team = UserTeamSerializer(data={'user':join_request.user.pk,
                                                                'team':join_request.team.pk,
                                                                'is_invited':False})
                serializer_user_team.is_valid(raise_exception=True)
                serializer_user_team.save()
            return Response(status=200, data={'result':'success'})
        
        except NotFoundJoinRequest as e:
            return Response(status=404, data={'error':str(e)})
        except NotFoundHackatonUser as e:
            return Response(status=404, data={'error':str(e)})