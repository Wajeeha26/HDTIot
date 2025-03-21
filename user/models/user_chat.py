from django.db import models

from chat.models.chat import Chat
from user.models.user import User


class UserChat(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return f"Chat {self.chat.id} - User {self.user.uid}"

    class Meta:
        db_table = "user_chat"
