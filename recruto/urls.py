from django.urls import path, include
from . import views
from .views import task_2

urlpatterns = [
    path('task1', views.task_1, name='task_1'),
    path('task2/', task_2.as_view(), name='generate_code'),
    path('auth/', include('rest_framework.urls')),
]