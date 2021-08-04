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
    start_time = datetime.datetime.now()
    old_slots = Schedule.objects.filter(datetime_slot__lt=start_time)
    logging.info(f'{len(old_slots)} old slots found.')

    archived_slots = [ArchiveSchedule(external_id=old_slots[i].id,
                                      master=old_slots[i].master,
                                      order=old_slots[i].order,
                                      datetime_slot=old_slots[i].datetime_slot)
                      for i in range(len(old_slots))]
    ArchiveSchedule.objects.bulk_create(archived_slots)
    logging.info(f'{len(archived_slots)} old slots archived.')

    Schedule.objects.filter(datetime_slot__lt=start_time).delete()
    logging.info(f'{len(old_slots)} old slots deleted.')


@app.task
def test_print() -> None:
    print('а я не живая!')
    logger.info('а я живая!')
