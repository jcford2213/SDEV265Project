from django.db import models
from django.conf import settings

class TrackedStock(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tracked_stocks = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.tracked_stocks}"
# Create your models here.
