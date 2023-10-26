"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView
from Hackaton.views import HackatonUserView, MyTeamListView, InviteTeamView, KickUserView, HackatonView
from Resume.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/v1/hackaton/user_registration/', HackatonUserView.as_view(), name='hackaton_user_registration'),
    path('api/v1/hackaton/my_team/', MyTeamListView.as_view(), name='hackaton_my_team'),
    path('api/v1/hackaton/invite/', InviteTeamView.as_view(), name='invite'),
    path('api/v1/hackaton/kick_user/', KickUserView.as_view(), name='kick_user'),
    path('api/v1/hackaton/info/', HackatonView.as_view(), name='hackaton_info'),


    path('resumes/<int:resume_id>/<str:model_name>/create/', CreateByResume.as_view(), name='create-by-resume'),
    path('resumes/<int:resume_id>/<str:model_name>/', RetrieveUpdateDestroyByResume.as_view(), name='detail-by-resume'),


    # #resume
    # path('api/v1/resume_RUD/<int:pk>/', RUD_ResumeByUser.as_view(),
    #      name='Get_Put_Delete_Resume_By_User_ID'), #получение resume по user_id
    #
    # path('api/v1/resume_create/<int:pk>/', Create_ResumeByUser.as_view(),
    #      name='Post_Resume_By_User_ID'), #создание resume по user_id
    #
    # path('api/v1/work_RUD/<int:pk>/', RUD_WorkByResume.as_view(),
    #      name='Get_Put_Delete_Work_By_Resume_ID'), #получение work по resume_id
    #
    # path('api/v1/work_create/<int:pk>/', Create_WorkByResume.as_view(),
    #      name='Post_Work_By_Resume_ID'), #создание work по resume_id
    #
    # path('api/v1/contact_RUD/<int:pk>/', RUD_СontactByResume.as_view(),
    #      name='Get_Put_Delete_Contact_By_ResumeID'), #получение contact по resume_id
    #
    # path('api/v1/contact_create/<int:pk>/', Create_ContactByResume.as_view(),
    #      name='Post_Contact_By_Resume_ID'), #создание contact по resume_id
    #
    # path('api/v1/hackatons_RUD/<int:pk>/', RUD_HackatonsByResume.as_view(),
    #      name='Get_Put_Delete_Hackatons_By_Resume_ID'), #получение hackatons по resume_id
    #
    # path('api/v1/hackatons_create/<int:pk>/', Create_HackatonsByResume.as_view(),
    #      name='Post_Hackatons_By_Resume_ID'), #создание hackatons по resume_id
    #
    # path('api/v1/educaion_RUD/<int:pk>/', RUD_EducationByResume.as_view(),
    #      name='Get_Put_Delete_Education_By_Resume_ID'), #получение education по resume_id
    #
    # path('api/v1/educaion_create/<int:resume_id>/', Create_EducationByResume.as_view(),
    #      name='Post_Education_By_Resume_ID'), #создание education по resume_id


]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
