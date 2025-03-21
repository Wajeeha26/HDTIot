from rest_framework import serializers

from user.models.user_chat import Chat, UserChat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"


class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChat
        fields = "__all__"
