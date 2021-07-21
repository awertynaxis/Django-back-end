from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models


class Master(models.Model):
    nickname = models.CharField(max_length=30, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    instagram = models.CharField(max_length=30, null=True, blank=True)
    master_telegram_id = models.CharField(max_length=15, null=True, blank=True)
    master_telegram_nickname = models.CharField(max_length=50, null=True, blank=True)
    master_phone_number = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='master', default=1)

    def __str__(self):
        return self.nickname


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
