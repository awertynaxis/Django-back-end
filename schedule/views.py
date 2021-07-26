from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

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


class ScheduleEdit(APIView):
    def get_object(self, pk):
        try:
            return Schedule.objects.get(pk=pk)
        except Schedule.DoesNotExist:
            raise Http404

    # TODO: right now POST request accepts full JSONs -- maybe it should accept
    #  `start date`, `end date`, `start time` and `end time` parameters
    #  so that full JSONs get created on back-end?
    def post(self, request):
        schedule_data = ScheduleSerializer(data=request.data, many=True)
        if schedule_data.is_valid():
            schedule_data.save()
            return Response(schedule_data.data)
        return Response(schedule_data.errors, status=status.HTTP_400_BAD_REQUEST)

    # for editing a single slot
    def patch(self, request):
        slot = self.get_object(request.data['id'])
        serializer = ScheduleSerializer(slot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # accepts a {'id'=___} JSON
    def delete(self, request):
        slot = self.get_object(request.data['id'])
        slot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
