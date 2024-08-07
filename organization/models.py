from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    is_client = models.BooleanField(default=False)

class Photo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='photos',blank=True,null=True)
    image = models.FileField(upload_to='uploads/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

