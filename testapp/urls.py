from django.conf.urls import url
from django.urls import re_path, path
from .views import  details_added_masters_view,list_added_masters_view

urlpatterns = [
    # path('addedmaster/', list_added_masters_view, name='addedmaster'),
    re_path('^addedmaster/(?P<pk>\d+)', list_added_masters_view, name='addedmaster-detail')
]
