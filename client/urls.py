from django.urls import re_path, path

from client.views import ClientView, ClientDetailsView, ClientRegisterView, ClientMasterListView, ClientMasterEditView,\
    CategoriesListView, MastersByCategoriesView, ClientMasterGetID

urlpatterns = [
    path('categories/', CategoriesListView.as_view(), name='categories_list'),
    path('categories/<category>', MastersByCategoriesView.as_view(), name='masters_by_categories'),
    path('clients/', ClientView.as_view(), name='client-list'),
    re_path(r'^clients/(?P<pk>\d+)$', ClientDetailsView.as_view(), name='client-details'),
    path('register/', ClientRegisterView.as_view(), name='client_register'),
    path('add_master/<telegram_id>', ClientMasterEditView.as_view(), name='client-master-edit'),
    path('add_master/get_id/', ClientMasterGetID.as_view(), name='client-master-get-id'),
    path('master_list/<telegram_id>', ClientMasterListView.as_view(), name='client-master-list'),
]
