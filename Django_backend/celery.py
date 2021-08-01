from celery import Celery
from celery.schedules import crontab
from django.conf import settings

app = Celery()

app.config_from_object(settings)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)
