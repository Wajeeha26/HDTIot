from django.db import models


class ChatHistory(models.Model):
    id = models.AutoField(primary_key=True)
    chat = models.ForeignKey(
        "accounts.Chat", on_delete=models.CASCADE
    )  # ✅ Correct reference
    prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.chat.id} History"
