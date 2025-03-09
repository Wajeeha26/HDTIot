from django.db import models

class Device(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class UserDevice(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("user.User", to_field="uid", on_delete=models.CASCADE)  # References uid
    device_uuid = models.TextField(null=True, blank=True)
    device_type = models.ForeignKey(Device, on_delete=models.CASCADE)
