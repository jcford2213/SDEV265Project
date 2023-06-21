## Database tables for the website

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

class savedTickers(models.Model):
    tickername = models.CharField(max_length=35)



