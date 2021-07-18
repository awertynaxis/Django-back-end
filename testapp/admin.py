from django.contrib import admin

# Register your models here.
from .models import Master, Client, AddedMasters


@admin.register(Master)
class Master(admin.ModelAdmin):
    fields = ('nick_name', 'first_name', 'last_name', 'instagram', 'telegram_id')


@admin.register(Client)
class Client(admin.ModelAdmin):
    fields = ('telegram_id', 'number', 'telegram_nickname',)


@admin.register(AddedMasters)
class AddedMasters(admin.ModelAdmin):
    fields = ('client', 'master',)
