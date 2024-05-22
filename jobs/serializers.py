from rest_framework import serializers

class JobSerializer(serializers.Serializer):
    title = serializers.CharField()
    company = serializers.CharField()
    location = serializers.CharField()
    description = serializers.CharField()
    url = serializers.CharField()
