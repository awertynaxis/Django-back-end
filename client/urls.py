from django.urls import re_path, path

from client.views import list_client_view, details_client_view

urlpatterns = [
    path('clients/', list_client_view, name='client-list'),
    re_path(r'^clients/(?P<pk>\d+)$', details_client_view, name='client-details'),

]