from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Sum


class Song(models.Model):
    singer = models.CharField(max_length=128, null=False, blank=False)
    song = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self):
        return f'{self.song}'


class RatingQuerySet(models.QuerySet):
    def big_o(self):
        return self.all().prefetch_related('user', 'song')


class RatingManager(models.Manager):
    def get_queryset(self):
        return RatingQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().big_o()

    def calc_list(self):
        return self.all().values('song__id', 'user__is_staff', 'song__song', 'song__singer'). \
            annotate(sum=Sum('rating'), count=Count('rating', distinct=True))


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='user_rating')
    song = models.ForeignKey(Song, on_delete=models.RESTRICT, related_name='song_rating')
    rating = models.IntegerField(null=False, blank=False)

    objects = RatingManager()
