from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated


from .serializers import ResumeSerializer, GraduationSerializer, EducationSerializer, WorkSerializer, ContactSerializer, HackatonsSerializer

from .models import Resume, Graduation, Education, Work, Contact, Hackatons





class RetrieveUpdateDestroyByResume(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        model_name = self.kwargs.get('model_name')
        resume_id = self.kwargs.get('resume_id')

        if model_name == 'resume':
            return Resume.objects.filter(id=resume_id)
        elif model_name == 'work':
            return Work.objects.filter(resume_id=resume_id)
        elif model_name == 'contact':
            return Contact.objects.filter(resume_id=resume_id)
        elif model_name == 'hackatons':
            return Hackatons.objects.filter(resume_id=resume_id)
        elif model_name == 'education':
            return Education.objects.filter(resume_id=resume_id)

    def get_serializer_class(self):
        model_name = self.kwargs.get('model_name')

        if model_name == 'resume':
            return ResumeSerializer
        elif model_name == 'work':
            return WorkSerializer
        elif model_name == 'contact':
            return ContactSerializer
        elif model_name == 'hackatons':
            return HackatonsSerializer
        elif model_name == 'education':
            return EducationSerializer




class CreateByResume(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        model_name = self.kwargs.get('model_name')
        resume_id = self.kwargs.get('resume_id')

        if model_name == 'resume':
            return Resume.objects.filter(id=resume_id)
        elif model_name == 'work':
            return Work.objects.filter(resume_id=resume_id)
        elif model_name == 'contact':
            return Contact.objects.filter(resume_id=resume_id)
        elif model_name == 'hackatons':
            return Hackatons.objects.filter(resume_id=resume_id)
        elif model_name == 'education':
            return Education.objects.filter(resume_id=resume_id)

    def get_serializer_class(self):
        model_name = self.kwargs.get('model_name')

        if model_name == 'resume':
            return ResumeSerializer
        elif model_name == 'work':
            return WorkSerializer
        elif model_name == 'contact':
            return ContactSerializer
        elif model_name == 'hackatons':
            return HackatonsSerializer
        elif model_name == 'education':
            return EducationSerializer




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


