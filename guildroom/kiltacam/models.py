from django.db import models

# Create your models here.

class Camera(models.Model):
    ip = models.CharField(max_length=15)
    position = models.IntegerField(default=0)
    name = models.TextField()
    current = models.ImageField(upload_to='cameras')