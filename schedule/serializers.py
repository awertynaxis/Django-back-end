from rest_framework import serializers

from schedule.models import Schedule, SortedSchedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_field = ('id',)


class SortedScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SortedSchedule
        fields = '__all__'
        read_only_field = ('id',)
