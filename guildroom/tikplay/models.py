from django.db import models

# Create your models here.
class Song(models.Model):
    video_id = models.TextField(default="")
    title = models.TextField(default="")
    description = models.TextField(default="")
    channel = models.TextField(default="")
    image = models.TextField(default="")
    position = models.IntegerField()

    class Meta:
        ordering = ['position']
        get_latest_by = 'position'

    def __str__(self):
        return "{} ({})".format(self.title, self.position)