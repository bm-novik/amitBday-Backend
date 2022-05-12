from django.contrib.auth.models import User
from django.db import models


class Song(models.Model):
    user = models.ManyToManyField(User, on_delete=models.RESTRICT, related_name='song')
    song_name = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self):
        return f'{self.song_name}'


class Rating (models.Model):
    class Rating(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name='rating')
    song = models.OneToOneField(User, on_delete=models.RESTRICT, related_name='rating')
    rating = models.IntegerField(choices=Rating.choices, null=False, blank=False)

