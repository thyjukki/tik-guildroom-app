from django.db import models

# Create your models here.
class Song(models.Model):
    url = models.URLField()
    audio_url = models.URLField()
    title = models.TextField()
    position = models.IntegerField()

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title + " " + (self.position)