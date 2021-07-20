from django.contrib import admin

# Register your models here.
from .models import Master, Client, Category, Service, Order, Schedule


@admin.register(Master)
class Master(admin.ModelAdmin):
    fields = ('username', 'first_name', 'last_name',
              'instagram', 'master_telegram_id', 'master_telegram_nickname',
              'master_phone_number', 'address',)


@admin.register(Category)
class Category(admin.ModelAdmin):
    fields = ('category_name',)


@admin.register(Service)
class Service(admin.ModelAdmin):
    fields = ('title', 'price', 'description', 'category', 'duration', 'master')


@admin.register(Client)
class Client(admin.ModelAdmin):
    fields = ('client_telegram_id', 'client_telegram_nickname', 'client_phone_number', 'master')


@admin.register(Order)
class Order(admin.ModelAdmin):
    fields = ('client', 'master', 'service')


@admin.register(Schedule)
class Schedule(admin.ModelAdmin):
    fields = ('master', 'order', 'datetime_slot')