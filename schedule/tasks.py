import datetime
import logging
from sys import stdout

from Django_backend.celery import app

logger = logging.getLogger()
# enabling console output for celery workers
logger.addHandler(logging.StreamHandler(stdout))


# TODO: order archivation task (maybe expand `archive_old_schedule_slots()` instead?)

@app.task
def archive_old_schedule_slots() -> None:
    """Fetches outdated schedule slots, adds them to the archive table and deletes them from the source table."""
    from schedule.models import Schedule, ArchiveSchedule
    from order.models import Order, ArchiveOrder
    start_time = datetime.datetime.now()
    old_slots = Schedule.objects.filter(datetime_slot__lt=start_time, order__isnull=False)
    old_orders = [Order.objects.filter(pk=x.order_id) for x in old_slots]
    #
    orders_to_archive = [ArchiveOrder(master=i[0].master,
                                      external_id=i[0].id,
                                      client=i[0].client,
                                      service=i[0].service) for i in old_orders]
    ArchiveOrder.objects.bulk_create(orders_to_archive)

    logging.info(f' {len(orders_to_archive)} old orders saved to OrderArchive.')

    archived_slots = [ArchiveSchedule(external_id=old_slots[i].id,
                                      master=old_slots[i].master,
                                      order=ArchiveOrder.objects.filter(external_id=old_slots[i].order_id).first(),
                                      datetime_slot=old_slots[i].datetime_slot)
                      for i in range(len(old_slots))]
    ArchiveSchedule.objects.bulk_create(archived_slots)
    logging.info(f'{len(archived_slots)} old slots archived.')

    Schedule.objects.filter(datetime_slot__lt=start_time).delete()
    logging.info(f'{len(old_slots)} old slots deleted (with order field not null).')
    #
    Order.objects.filter(order__isnull=True).delete()
    logging.info(f'{len(old_orders)} old slots archived.')


@app.task
def test_print() -> None:
    print('а я не живая!')
    logger.info('а я живая!')
