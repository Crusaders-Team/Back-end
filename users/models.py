from django.db import models
from django.contrib.auth.models import AbstractUser

from core.settings import MEDIA_ROOT


class CustomUser(AbstractUser):
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='media/', default=f'{MEDIA_ROOT}/default.jpg')


# Create your models here.
