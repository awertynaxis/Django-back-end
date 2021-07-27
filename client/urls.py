from django.urls import re_path, path

from client.views import list_client_view, details_client_view, \
    ClientRegisterView, ClientMasterListView, ClientMasterEditView, CategoriesListView, MastersByCategoriesView, \
    ClientMasterGetID

urlpatterns = [
    path('clients/', list_client_view, name='client-list'),
    re_path(r'^clients/(?P<pk>\d+)$', details_client_view, name='client-details'),
    path('clients/register/', ClientRegisterView.as_view()),
    path('clients/add_master/<telegram_id>', ClientMasterEditView.as_view()),
    path('clients/add_master/get_id/', ClientMasterGetID.as_view()),
    path('clients/master_list/<telegram_id>/', ClientMasterListView.as_view()),
    path('categories/', CategoriesListView.as_view()),
    path('categories/<category>', MastersByCategoriesView.as_view())
]
