from django.urls import path, include
from .views import TeamView, HackatonUserView, InviteTeamView, KickUserView, HackatonUrlInvite, HackatonListView, HackatonCreateView, JoinRequestView
from rest_framework import routers


urlpatterns = [
    path('request_join_team/', JoinRequestView.as_view({'put':'request_join_team', 
                                                        'get':'get_list_requests',
                                                        'patch':'answer_request'})),
    path('user_registration/', HackatonUserView.as_view({'post':'post',})),
    path('get_hackaton_users/', HackatonUserView.as_view({'get':'get_hackaton_users'})),
    path('my_team_list/', TeamView.as_view({'get':'my_team_list'})),
    path('invite/', InviteTeamView.as_view(), name='invite'),
    path('kick_user/', KickUserView.as_view(), name='kick_user'),
    path('get_team_list/', TeamView.as_view({'get':'team_list'})),
    path('create_team/', TeamView.as_view({'post':'create_team'})),
    path('invite_url/', HackatonUrlInvite.as_view(), name='invite_url'),
    path('get_hackatons/', HackatonListView.as_view({'get':'list'}), name='get_hackatons'),
    path('create_hacakton/', HackatonCreateView.as_view(), name='create_hacakton'),
    path('get_locations/', HackatonListView.as_view({'get':'get_locations'})),
]

