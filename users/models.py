from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=40)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=250,unique=True)
    password = models.CharField(max_length=250)
    phone = models.CharField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = "users"
