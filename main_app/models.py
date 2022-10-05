from django.db import models
from django.urls import reverse # reverse lookup- URL path builder
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

