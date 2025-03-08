from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, uid, email, first_name, last_name, user_type=1, is_deleted=0, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(uid=uid, email=self.normalize_email(email), first_name=first_name, last_name=last_name, user_type=user_type, is_deleted=is_deleted)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    uid = models.CharField(max_length=255, unique=True, primary_key=True)  # Changed to uid
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    user_type = models.IntegerField(default=1)
    is_deleted = models.IntegerField(default=0)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['uid', 'first_name', 'last_name']

    def __str__(self):
        return self.first_name
