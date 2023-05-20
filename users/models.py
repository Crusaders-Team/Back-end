from django.db import models
import hashlib


from django.contrib.auth.models import AbstractUser,User

class CustomUser(AbstractUser):
    username=models.CharField(max_length=30,unique=True)
    email=models.EmailField(unique=True)
    # password=models.CharField(max_length=64)
    avatar=models.ImageField(upload_to='avatars/',default='../avatars/avatars/default.jpg')
    REQUIRED_FIELDS=['email', 'password','avatar',]
    USERNAME_FIELD='username'
    
    # def create_user(self,username,email,password):
    #     self.username=username
    #     self.email=email
    #     self.password=hashlib.sha256(password.encode()).hexdigest()
    #     self.save()
    # def __str__(self):
    #     return self.username



# Create your models here.
