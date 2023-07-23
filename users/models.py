from django.db import models
import json

class User(models.Model):
    username = models.CharField(max_length=25, unique=True)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    tracked_stocks = models.TextField(blank=True, max_length=500)