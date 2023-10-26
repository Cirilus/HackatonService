from rest_framework import serializers
from .models import Resume, Graduation, Education, Work, Contact, Hackatons

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'

class GraduationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graduation
        fields = '__all__'

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class HackatonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackatons
        fields = '__all__'

