from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models


class Master(models.Model):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    instagram = models.CharField(max_length=30, null=True, blank=True)
    master_telegram_id = models.CharField(max_length=15, null=True, blank=True)
    master_telegram_nickname = models.CharField(max_length=50, null=True, blank=True)
    master_phone_number = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    category_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.category_name


class Service(models.Model):
    title = models.CharField(max_length=256)
    price = models.CharField(max_length=10)
    description = models.TextField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    duration = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.title


class Client(models.Model):
    client_telegram_id = models.CharField(max_length=15)
    client_telegram_nickname = models.CharField(max_length=50, blank=True, null=True)
    client_phone_number = models.CharField(max_length=14, blank=True, null=True)
    master = models.ManyToManyField(Master, related_name='clients', blank=True)

    def __str__(self):
        return self.client_telegram_id


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client')
    master = models.ForeignKey(Master, on_delete=models.CASCADE,  related_name='masters')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='publicservice')

    def __str__(self):
        return f"Заказ №{self.id}"


class Schedule(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='schedule')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='order')
    datetime_slot = models.DateTimeField()

    def __str__(self):
        return str(self.id)

# Create your models here.
