from django.urls import re_path, path

from client.views import list_client_view, details_client_view, ClientMasterListView

urlpatterns = [
    path('clients/', list_client_view, name='client-list'),
    re_path(r'^clients/(?P<pk>\d+)$', details_client_view, name='client-details'),
    path('clients/master_list/<int:pk>/', ClientMasterListView.as_view())
]
