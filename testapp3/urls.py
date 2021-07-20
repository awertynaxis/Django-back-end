from django.urls import re_path, path

from .views import list_client_view, list_master_view

urlpatterns = [
    path('clients/', list_client_view, name='client-list'),
    # re_path(r'^makes/(?P<pk>\d+)$', details_make_view, name='make-details'),
    path('masters/', list_master_view, name='master-list'),
    # re_path(r'models/(?P<pk>\d+)', details_model_view, name='model-details'),
]
