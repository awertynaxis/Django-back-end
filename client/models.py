from django.db import models
from master.models import Master


class Client(models.Model):
    client_telegram_id = models.CharField(max_length=15, unique=True)
    client_telegram_nickname = models.CharField(max_length=50, blank=True, null=True)
    client_phone_number = models.CharField(max_length=14, blank=True, null=True)
    master = models.ManyToManyField(Master, related_name='clients', blank=True)

    def __str__(self):
        return self.client_telegram_id
