from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class MyUser(AbstractUser):
    name=models.CharField(max_length=200)
    email=models.EmailField(unique=True)
    mobile=models.CharField(max_length=15,unique=True)

    
class Post(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    no_of_likes=models.ManyToManyField(MyUser,related_name="likes")
    description=models.CharField(max_length=400)
    tags=models.ManyToManyField(MyUser,related_name='tagged_users',blank=True)
    date=models.DateTimeField(auto_now_add=True)
