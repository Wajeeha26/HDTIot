from django.db import models

class Service(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    pricing = models.CharField(max_length=200, default="100")

    def __str__(self):
        return self.name

class UserService(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("user.User", to_field="uid", on_delete=models.CASCADE)  # References uid
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"User {self.user.uid} - Service {self.service.id}"
