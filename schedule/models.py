from django.db import models
from master.models import Master
from order.models import Order, ArchiveOrder


class Schedule(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='schedule')
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='order')
    datetime_slot = models.DateTimeField()

    def __str__(self):
        return str(self.id)


class SortedSchedule(models.Model):
    external_id = models.BigIntegerField()
    master = models.ForeignKey(Master, on_delete=models.DO_NOTHING, related_name='sorted_schedule')
    datetime_slot = models.DateTimeField()

    class Meta:
        managed = False

    def __str__(self):
        return str(self.id)


# used for archivation celery task
class ArchiveSchedule(models.Model):
    external_id = models.BigIntegerField()
    master = models.ForeignKey(Master, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(ArchiveOrder, on_delete=models.DO_NOTHING, null=True, blank=True)
    datetime_slot = models.DateTimeField()

    def __str__(self):
        return str(self.id)
