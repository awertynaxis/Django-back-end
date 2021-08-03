import datetime
import logging
from sys import stdout
from typing import List

from Django_backend.celery import app

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(stdout))


@app.task
def archive_old_schedule_slots() -> None:
    from schedule.models import Schedule, ArchiveSchedule
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


@app.task
def test_print():
    print('а я не живая!')
    logger.info('а я живая!')
