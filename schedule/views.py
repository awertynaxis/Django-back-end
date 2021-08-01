from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from schedule.models import Schedule, SortedSchedule
from schedule.serializers import ScheduleSerializer, SortedScheduleSerializer


class ScheduleList(generics.ListCreateAPIView):
    """Gives a list of all schedule slots.
    Implemented for debug purposes and isn't used by any clients."""
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


# TODO: a debug purposes view that gives a list of all free slots that are in the future

class ScheduleMasterList(generics.ListAPIView):
    """Gives all free slots of a specified (by `master_id`) master."""
    serializer_class = SortedScheduleSerializer

    def get_queryset(self):
        # taking keyword argument from address
        master = self.kwargs['master_id']
        # filtering all free slots by master's ID
        return SortedSchedule.objects.filter(master_id=master)


class ScheduleEdit(APIView):
    """Sends, edits and deletes schedule slots."""
    def get_object(self, pk):
        try:
            return Schedule.objects.get(pk=pk)
        except Schedule.DoesNotExist:
            raise Http404

    # POST request accepts full JSONs
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
