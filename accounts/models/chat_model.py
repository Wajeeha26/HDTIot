from django.db import models

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id}"

class UserChat(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("accounts.User", to_field="uid", on_delete=models.CASCADE)  # References uid
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return f"Chat {self.chat.id} - User {self.user.uid}"
