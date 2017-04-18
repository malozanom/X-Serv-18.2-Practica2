from django.db import models

# Create your models here.

class ShortenUrls(models.Model):
    longUrl = models.CharField(max_length=50)
    shortUrl = models.CharField(max_length=50)
