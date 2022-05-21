from django.contrib.auth.models import User
from django.db import models


class Song(models.Model):
    singer = models.CharField(max_length=128, null=False, blank=False)
    song = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self):
        return f'{self.song}'


class Rating (models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='rating')
    song = models.ForeignKey(Song, on_delete=models.RESTRICT, related_name='rating')
    rating = models.IntegerField(null=False, blank=False)

