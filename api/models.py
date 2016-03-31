from __future__ import unicode_literals
from django.db import models


class DeviceToken(models.Model):
    token = models.CharField(max_length=256, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.token


class Schedule(models.Model):
    date = models.DateField(unique=True)
    opponent = models.CharField(max_length=256)
    url = models.URLField(max_length=500)
    home_game = models.BooleanField()
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    def __unicode__(self):
        return self.url

