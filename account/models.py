from django.db import models


# Create your models here.
class Rsvp(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    guest_name = models.CharField(max_length=128, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    plus_one = models.BooleanField(default=False)
    song = models.CharField(max_length=128, null=True, blank=True)


class Permission(models.Model):
    permission = models.BooleanField(default=False)
