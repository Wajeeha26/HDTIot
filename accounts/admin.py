from django.contrib import admin

from accounts.models.chat_history_model import ChatHistory
from accounts.models.chat_model import Chat, UserChat
from accounts.models.service_model import Service, UserService
from accounts.models.user_model import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "uid",
        "email",
        "user_type",
        "is_deleted",
    )  # Removed 'id', changed 'role' to 'user_type'
    list_filter = ("user_type", "is_deleted")
    search_fields = ("uid", "email")


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")  # Changed 'chat_id' to 'id'
    search_fields = ("id",)


@admin.register(UserChat)
class UserChatAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "chat")  # Changed 'uid' to 'user'
    list_filter = ("user",)
    search_fields = ("user__uid", "chat__id")  # Fixed references


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "pricing")  # Fixed fields
    list_filter = ("pricing",)
    search_fields = ("name", "description")


@admin.register(UserService)
class UserServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "service")  # Changed 'uid' to 'user'
    list_filter = ("user", "service")
    search_fields = ("user__uid", "service__name")  # Fixed references


@admin.register(ChatHistory)  # Added ChatHistory Admin
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "chat", "prompt", "response", "created_at")
    list_filter = ("chat", "created_at")
    search_fields = ("chat__id", "prompt", "response")
