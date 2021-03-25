from django.db import models

# Create your models here.
class Log(models.Model):
    username = models.CharField(max_length=30)
    dateTime = models.CharField(max_length=100)
    startTime = models.CharField(max_length=100)
    endTime = models.CharField(max_length=100)
    url = models.CharField(max_length=255, blank=True)