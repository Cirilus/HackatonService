from django.urls import path, include
from .views import UserView


urlpatterns = [
    path('action_user/', UserView.as_view(), name='action_user'),
]