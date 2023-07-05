from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

class SavedTicker(models.Model): ## SavedTicker is a database for the Users saved tickers on their account.
    ## ForeignKey defines a "Many-to-one" relationship to the user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tickername = models.CharField(max_length=35)
