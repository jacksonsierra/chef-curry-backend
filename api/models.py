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
    has_started = models.BooleanField(default=False)
    has_finished = models.BooleanField(default=False)
    state = models.CharField(max_length=256, default='none')

    def __unicode__(self):
        return self.url


class Stats(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    minutes_elapsed = models.PositiveSmallIntegerField(null=True)
    minutes_played = models.PositiveSmallIntegerField(null=True)
    seconds_played = models.PositiveSmallIntegerField(null=True)
    field_goals_made = models.PositiveSmallIntegerField(null=True)
    field_goals_attempted = models.PositiveSmallIntegerField(null=True)
    three_pointers_made = models.PositiveSmallIntegerField(null=True)
    three_pointers_attempted = models.PositiveSmallIntegerField(null=True)
    free_throws_made = models.PositiveSmallIntegerField(null=True)
    free_throws_attempted = models.PositiveSmallIntegerField(null=True)
    plus_minus = models.CharField(max_length=20, null=True)
    offensive_rebounds = models.PositiveSmallIntegerField(null=True)
    defensive_rebounds = models.PositiveSmallIntegerField(null=True)
    total_rebounds = models.PositiveSmallIntegerField(null=True)
    assists = models.PositiveSmallIntegerField(null=True)
    turnovers = models.PositiveSmallIntegerField(null=True)
    steals = models.PositiveSmallIntegerField(null=True)
    blocks = models.PositiveSmallIntegerField(null=True)
    blocks_against = models.PositiveSmallIntegerField(null=True)
    personal_fouls = models.PositiveSmallIntegerField(null=True)
    points = models.PositiveSmallIntegerField(null=True)
