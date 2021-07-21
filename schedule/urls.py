from django.urls import path

from schedule.views import ScheduleList, ScheduleMasterList

urlpatterns = [
    path('', ScheduleList.as_view()),
    path('by_master/<master_id>', ScheduleMasterList.as_view())
]
