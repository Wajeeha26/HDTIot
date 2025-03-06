from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, uid, email, role):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(uid=uid, email=self.normalize_email(email), role=role)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    uid = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[('patient', 'Patient'), ('doctor', 'Doctor')])
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['uid']

