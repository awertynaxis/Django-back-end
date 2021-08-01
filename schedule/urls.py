from django.urls import path

from schedule.views import ScheduleList, ScheduleMasterList, ScheduleEdit

urlpatterns = [
    path('', ScheduleList.as_view(), name='schedule-list'),
    path('by_master/<master_id>', ScheduleMasterList.as_view(), name='schedule-by-master-list'),
    path('edit/', ScheduleEdit.as_view(), name='schedule-edit')
]
