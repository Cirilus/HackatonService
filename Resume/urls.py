
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

from django.urls import path, include

from rest_framework.routers import SimpleRouter

from Resume.views import *

router_resume = SimpleRouter()
router_resume.register(r'resumelist', ResumeCRUD)

router_work = SimpleRouter()
router_work.register(r'worklist', WorkCRUD)

router_contact = SimpleRouter()
router_contact.register(r'contactlist', ContactCRUD)

router_hackatons = SimpleRouter()
router_hackatons.register(r'hackatonslist', HackatonsCRUD)

router_education = SimpleRouter()
router_education.register(r'educationlist', EducationCRUD)

router_graduation = SimpleRouter()
router_graduation.register(r'graduationlist', GraduationCRUD)

urlpatterns = [
    path('api/v1/', include(router_resume.urls)), # http://127.0.0.1:8000/api/v1/resumelist/ (<int:pk>/) запись по своему id
    path('api/v1/', include(router_work.urls)),  # http://127.0.0.1:8000/api/v1/worklist/ (<int:resume_id>/)
    path('api/v1/', include(router_contact.urls)),  # http://127.0.0.1:8000/api/v1/contactlist/ (<int:resume_id>/)
    path('api/v1/', include(router_hackatons.urls)),  # http://127.0.0.1:8000/api/v1/hackatonslist/ (<int:resume_id>/)
    path('api/v1/', include(router_education.urls)),  # http://127.0.0.1:8000/api/v1/educationlist/ (<int:resume_id>/)
    path('api/v1/', include(router_graduation.urls)),  # http://127.0.0.1:8000/api/v1/graduationlist/ (<int:pk>/)

    path('api/v1/resumelist/byuserid/<int:user_id>/', ResumeCRUD.as_view({'get': 'byuserid', 'delete': 'byuserid',
                                                                          'put': 'byuserid'})),

    path('api/v1/worklist/byresumeid/<int:resume_id>/', WorkCRUD.as_view({'get': 'byresumeid'})),

    path('api/v1/contactlist/byresumeid/<int:resume_id>/', ContactCRUD.as_view({'get': 'byresumeid'})),

    path('api/v1/hackatonslist/byresumeid/<int:resume_id>/', HackatonsCRUD.as_view({'get': 'byresumeid'})),

    path('api/v1/educationlist/byresumeid/<int:resume_id>/', EducationCRUD.as_view({'get': 'byresumeid'})),


    path('helpcd/', cd_test_endpoint, name='cd_test_endpoint'),

]

