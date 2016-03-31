from __future__ import unicode_literals
from django.db import models


class DeviceToken(models.Model):
    token = models.CharField(max_length=256, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.token
