from django.db import models
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Master(models.Model):
    nick_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    instagram = models.CharField(max_length=255)
    telegram_id = models.CharField(max_length=100)

    def __str__(self):
        return self.nick_name


class Client(models.Model):
    telegram_id = models.CharField(max_length=100)
    number = models.CharField(max_length=100, blank=True)
    telegram_nickname = models.CharField(max_length=100)

    def __str__(self):
        return self.telegram_nickname


class AddedMasters(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client')
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='master')

    def __str__(self):
        return f'{self.master}/{self.client}'
