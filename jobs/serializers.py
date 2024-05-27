from rest_framework import serializers
from .models import Job, JobApplication
from django.contrib.auth.models import User
class JobSerializer(serializers.Serializer):
    title = serializers.CharField()
    company = serializers.CharField()
    location = serializers.CharField()
    description = serializers.CharField()
    url = serializers.CharField()

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'user', 'cover_letter', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user
