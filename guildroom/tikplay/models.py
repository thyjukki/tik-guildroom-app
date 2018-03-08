from django.db import models

# Create your models here.
class Song:
    url = models.URLField()
    audio_url = models.URLField()
    title = models.CharField()