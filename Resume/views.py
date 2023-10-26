from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated


from .serializers import ResumeSerializer, GraduationSerializer, EducationSerializer, WorkSerializer, ContactSerializer, HackatonsSerializer

from .models import Resume, Graduation, Education, Work, Contact, Hackatons








#получение resume по user_id
class RUD_ResumeByUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny,]
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

#создание resume по user_id
class Create_ResumeByUser(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


#получение work по resume_id
class RUD_WorkByResume(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny,]
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

#создание work по resume_id
class Create_WorkByResume(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    queryset = Work.objects.all()
    serializer_class = WorkSerializer


#получение contact по resume_id
class RUD_СontactByResume(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny,]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

#создание contact по resume_id
class Create_ContactByResume(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

#получение hackatons по resume_id
class RUD_HackatonsByResume(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny,]
    queryset = Hackatons.objects.all()
    serializer_class = HackatonsSerializer

#создание contact по resume_id
class Create_HackatonsByResume(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    queryset = Hackatons.objects.all()
    serializer_class = HackatonsSerializer


#получение education по resume_id
class RUD_EducationByResume(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny,]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

#получение education по resume_id
class Create_EducationByResume(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


#получение education по graduation_id
class RUD_EducationByGraduation(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny,]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

#добавление education по graduation_id
class Create_EducationByGraduation(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


