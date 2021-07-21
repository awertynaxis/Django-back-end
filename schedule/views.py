from django.shortcuts import render
from rest_framework import generics

from schedule.models import Schedule
from schedule.serializers import ScheduleSerializer


# this view is here for debug purposes and isn't used by any clients
class ScheduleList(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class ScheduleMasterList(generics.ListAPIView):
    serializer_class = ScheduleSerializer

    # TODO: refactor this into using DB views
    def get_queryset(self):
        # taking keyword argument from address
        master = self.kwargs['master_id']
        # filtering all slots by master's ID
        return Schedule.objects.filter(master_id=master)
