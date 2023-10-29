from rest_framework import serializers
from .models import Resume, Graduation, Education, Work, Contact, Hackatons

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['user', 'title', 'description','visible','id']

class GraduationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graduation
        fields = ['id', 'title']

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['resume',  'graduation', 'id', 'title', 'begin', 'end']


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ['resume', 'id', 'title', 'description', 'begin', 'end']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['resume', 'id', 'title', 'body']

class HackatonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackatons
        fields = ['resume', 'id', 'title', 'description','begin', 'end', 'place']

