from django.db import models
from master.models import Master
from order.models import Order


class Schedule(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='schedule')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='order')
    datetime_slot = models.DateTimeField()

    def __str__(self):
        return str(self.id)
