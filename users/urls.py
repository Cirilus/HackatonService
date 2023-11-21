from django.urls import path, include
from .views import UserViewSet
from rest_framework.routers import SimpleRouter


router_user = SimpleRouter()
router_user.register(r'userlist', UserViewSet)


urlpatterns = [
    path('action_user/', include(router_user.urls)),
]