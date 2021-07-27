from django.db import models
from master.models import Master, Service
from client.models import Client


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client')
    master = models.ForeignKey(Master, on_delete=models.CASCADE,  related_name='masters')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='publicservice')

    def __str__(self):
        return f"Заказ №{self.id}"

