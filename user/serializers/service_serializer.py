from rest_framework import serializers
from user.models.service_model import Service, UserServices

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class UserServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserServices
        fields = '__all__'