from django.urls import re_path, path

from client.views import list_client_view, details_client_view, \
    ClientMasterListView, CategoriesListView, MastersByCategoriesView

urlpatterns = [
    path('clients/', list_client_view, name='client-list'),
    re_path(r'^clients/(?P<pk>\d+)$', details_client_view, name='client-details'),
    path('clients/master_list/<telegram_id>/', ClientMasterListView.as_view()),
    path('categories/', CategoriesListView.as_view()),
    path('categories/<category>', MastersByCategoriesView.as_view())
]
