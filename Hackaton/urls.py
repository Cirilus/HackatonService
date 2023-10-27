from django.urls import path, include
from .views import TeamView, HackatonUserView, MyTeamListView, InviteTeamView, KickUserView, HackatonView, HackatonUrlInvite, HackatonListApi
from rest_framework import routers

urlpatterns = [
    path('user_registration/', HackatonUserView.as_view(), name='hackaton_user_registration'),
    path('my_team_list/', MyTeamListView.as_view(), name='hackaton_my_team_list'),
    path('invite/', InviteTeamView.as_view(), name='invite'),
    path('token_invite/', HackatonUrlInvite.as_view(), name='invite'),
    path('kick_user/', KickUserView.as_view(), name='kick_user'),
    path('info/', HackatonView.as_view(), name='hackaton_info'),
    path('get_team/', TeamView.as_view(), name='get_my_team'),
    path('invite_url/', HackatonUrlInvite.as_view(), name='invite_url'),
    path('get_hackatons/', HackatonListApi.as_view(), name='get_hackatons')
]

