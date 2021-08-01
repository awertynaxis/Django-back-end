import datetime
import logging
from typing import List

from celery import shared_task

from schedule.models import Schedule, ArchiveSchedule


logger = logging.getLogger()


@shared_task(
    name='schedule.archive_old_slots',
    # queue='schedule',
    soft_time_limit=60,
)
def archive_old_schedule_slots() -> None:
    start_time = datetime.datetime.now()
    old_slots = Schedule.objects.filter(datetime_slot__lt=start_time)
    logging.info(f'{len(old_slots)} old slots found.')
    archived_slots = ArchiveSchedule.objects.bulk_create(old_slots)
    logging.info(f'{len(archived_slots)} old slots archived.')
    for i in len(archived_slots):
        archived_slots[i].external_id = old_slots[i].id
    ArchiveSchedule.objects.bulk_update(archived_slots, ['external_id'])
    logging.info(f'{len(archived_slots)} archived slots updated.')
    Schedule.objects.filter(datetime_slot__lt=start_time).delete()
    logging.info(f'{len(old_slots)} old slots deleted.')


@shared_task(
    name='schedule.archive_slots',
)
def test_print() -> None:
    logger.info('а я живая!')
