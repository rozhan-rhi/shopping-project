from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=250,unique=True)
    password = models.CharField(max_length=250)
    phone = models.CharField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []