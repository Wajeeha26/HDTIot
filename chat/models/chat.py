from django.db import models


class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    def __str__(self):
        return f"Chat {self.id}"

    class Meta:
        db_table = "chat"


class ChatHistory(models.Model):
    id = models.AutoField(primary_key=True)
    chat_id = models.ForeignKey("Chat", on_delete=models.CASCADE, db_column="chat_id")
    prompt = models.TextField(null=False, blank=False, db_column="prompt")
    response = models.TextField(null=False, blank=False, db_column="response")
    created_at = models.DateTimeField(
        null=False, auto_now_add=True, db_column="created_at"
    )

    def __str__(self):
        return f"Chat {self.chat.id} History"

    class Meta:
        db_table = "chat_history"
