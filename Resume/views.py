
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated


from .serializers import ResumeSerializer, GraduationSerializer, EducationSerializer, WorkSerializer, ContactSerializer, HackatonsSerializer

from .models import Resume, Graduation, Education, Work, Contact, Hackatons


#получение списка всех объектов, получение создание удаление изменение объектов по user_id
class ResumeByUserCRUD(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    lookup_field = 'user_id'


#получение списка всех объектов, получение создание удаление изменение объектов по resume_id
class WorkByResumeCRUD(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    lookup_field = 'resume_id'

#получение списка всех объектов, получение создание удаление изменение объектов по resume_id
class ContactByResumeCRUD(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    lookup_field = 'resume_id'

#получение списка всех объектов, получение создание удаление изменение объектов по resume_id
class HackatonsByResumeCRUD(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Hackatons.objects.all()
    serializer_class = HackatonsSerializer
    lookup_field = 'resume_id'



#получение списка всех объектов, получение создание удаление изменение объектов по resume_id
class EducationByResumeCRUD(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    lookup_field = 'resume_id'

#получение списка всех объектов, получение создание удаление изменение объектов по id
class GraduationCRUD(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Graduation.objects.all()
    serializer_class = GraduationSerializer


