from rest_framework import serializers

from user.models.service_model import Service, UserService


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class UserServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserService
        fields = "__all__"
