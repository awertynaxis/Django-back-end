from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db import models


class Masters(models.Model):
    username = models.CharField(max_length=30, unique=True)
    first_names = models.CharField(max_length=64, null=True, blank=True)
    last_names = models.CharField(max_length=64, null=True, blank=True)
    instagram = models.CharField(max_length=30, null=True, blank=True)
    telegram_id = models.CharField(max_length=15, null=True, blank=True)
    telegram_nickname = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username


class Categories(models.Model):
    category = models.CharField(max_length=100, null=True)


class Service(models.Model):
    title = models.CharField(max_length=256, null=True)
    price = models.CharField(max_length=10, null=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='categories')
    duration = models.IntegerField(null=True)
    master_id = models.ForeignKey(Masters, on_delete=models.CASCADE, related_name='master')


class Clients(models.Model):
    telegram_id = models.CharField(max_length=15, null=True)
    number = models.CharField(max_length=14, blank=True, null=True)
    telegram_nickname = models.CharField(max_length=50, blank=True, null=True)
    master = models.ManyToManyField(Masters, related_name='clients')
    #Добавить поле many to many мастеров сюда , мастерв , релейтед клаинтс

    def __str__(self):
        return self.telegram_nickname


class Order(models.Model):
    client_id = models.OneToOneField(Clients, on_delete=models.CASCADE, related_name='client')
    master_id = models.OneToOneField(Masters, on_delete=models.CASCADE, related_name='masters')
    service_id = models.OneToOneField(Service, on_delete=models.CASCADE, related_name='publicservice')
    date_time = models.DateTimeField()


class Schedule(models.Model):
    master = models.ForeignKey(Masters, on_delete=models.CASCADE, related_name='masterss')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='order')
    date_time = models.DateTimeField()

# Create your models here.
