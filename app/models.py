from django.contrib.auth.models import AbstractUser
from django.db import models
from . manager import CustomUserManager

class User(AbstractUser):
    
    email_verified = models.BooleanField(default=False)