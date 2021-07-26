from django.urls import path

from schedule.views import ScheduleList, ScheduleMasterList, ScheduleEdit

urlpatterns = [
    path('', ScheduleList.as_view()),
    path('by_master/<master_id>', ScheduleMasterList.as_view()),
    path('edit/', ScheduleEdit.as_view())
]
