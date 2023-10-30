from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView
from Hackaton.views import HackatonUserView, MyTeamListView, InviteTeamView, KickUserView, HackatonView
from Resume.views import *


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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.routers import SimpleRouter

from Resume.views import *


router_resume = SimpleRouter()
router_resume.register(r'resumelist', ResumeByUserCRUD)

router_work = SimpleRouter()
router_work.register(r'worklist', WorkByResumeCRUD)

router_contact = SimpleRouter()
router_contact.register(r'contactlist', ContactByResumeCRUD)

router_hackatons = SimpleRouter()
router_hackatons.register(r'hackatonslist', HackatonsByResumeCRUD)

router_education = SimpleRouter()
router_education.register(r'educationlist', EducationByResumeCRUD)

router_graduation = SimpleRouter()
router_graduation.register(r'graduationlist', GraduationCRUD)

urlpatterns = [
    path('api/v1/', include(router_resume.urls)), #http://127.0.0.1:8000/api/v1/resumelist/ (<int:user_id>/)
    path('api/v1/', include(router_work.urls)), #http://127.0.0.1:8000/api/v1/worklist/ (<int:resume_id>/)
    path('api/v1/', include(router_contact.urls)), #http://127.0.0.1:8000/api/v1/contactlist/ (<int:resume_id>/)
    path('api/v1/', include(router_hackatons.urls)), #http://127.0.0.1:8000/api/v1/hackatonslist/ (<int:resume_id>/)
    path('api/v1/', include(router_education.urls)), #http://127.0.0.1:8000/api/v1/educationlist/ (<int:resume_id>/)
    path('api/v1/', include(router_graduation.urls)), #http://127.0.0.1:8000/api/v1/graduationlist/ (<int:pk>/)
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
