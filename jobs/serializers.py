from rest_framework import serializers
from .models import Job, JobApplication
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
