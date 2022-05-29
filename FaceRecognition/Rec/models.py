from distutils.command.upload import upload
from unicodedata import name
from django.db import models
import os

# Create your models here.
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MEDIA_ROOT = os.path.join(BASE_DIR,'MovieImages\\')

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    lower_age = models.IntegerField()
    upper_age = models.IntegerField()
    poster = models.ImageField(upload_to = 'MovieImages/')

    def __str__(self):
        return f" {self.name}"

class UserProfile(models.Model):
    username = models.CharField(max_length=64, primary_key=True)
    profile = models.ImageField(upload_to = 'ProfileImages/')