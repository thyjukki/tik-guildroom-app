from django.db import models

# Create your models here.
class Song(models.Model):
    video_id = models.TextField(default="")
    title = models.TextField(default="")
    description = models.TextField(default="")
    channel = models.TextField(default="")
    image = models.TextField(default="")
    position = models.IntegerField()
    audio_url = models.TextField(default="")
    added_by = models.TextField(default="")

    class Meta:
        ordering = ['position']
        get_latest_by = 'position'

    def __str__(self):
        return "{} ({})".format(self.title, self.position)

# Model to keep track of played songs
class Log(models.Model):
    video_id = models.TextField(default="")
    added_by = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)

