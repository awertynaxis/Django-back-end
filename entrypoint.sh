#!/usr/bin/bash

echo "Running migrations"
./manage.py migrate

echo "Running tests"
./manage.py test order.tests
./manage.py test client.tests
./manage.py test master.tests
./manage.py test schedule.tests

echo "Running server"
./manage.py runserver 0.0.0.0:8000

#echo "Running beatschedule"
#function start_beat() {
#    celery -A Django_backend.celery beat
#}
#
#
#echo "Running workers"
#function start_worker() {
#    celery -A Django_backend.celery worker --loglevel=INFO -n worker2@%h
#}
#
#
#echo "Running flower"
#function start_flower() {
#    celery -A Django_backend flower --address=127.0.0.6 --port=5566
#}
#
#case $SERVICE in
#backend)
#  start_beat
#  start_worker
#  start_flower
#  ;;
#esac
