from django.db import models
from master.models import Master, Service
from client.models import Client


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client')
    master = models.ForeignKey(Master, on_delete=models.CASCADE,  related_name='masters')
    # TODO: rename 'publicservice'
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='publicservice')

    def __str__(self):
        return f"Заказ №{self.id}"


# used for archivation celery task
class ArchiveOrder(models.Model):
    external_id = models.BigIntegerField(default=1)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    master = models.ForeignKey(Master, on_delete=models.DO_NOTHING)
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'Архивированный Заказ № {self.id} '
