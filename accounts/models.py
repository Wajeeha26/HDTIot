from django.db import models

class User(models.Model):
    uid = models.CharField(max_length=255, unique=True)  # Firebase UID
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=[('patient', 'Patient'), ('doctor', 'Doctor')])

    def __str__(self):
        return self.email
