from .models import User, Feedback
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    # разобраться что сериализатор делает с полем даты create_at
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'contact_back', 'feedback_massage', 'create_at', 'status']

