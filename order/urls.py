from django.urls import re_path, path

from order.views import OrderListView, OrderDetailView, OrderCreateView, OrderMasterListView
    # list_order_view, detail_order_view, create_order_view, list_order_master_view

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    re_path(r'^orders/(?P<pk>\d+)$', OrderDetailView.as_view(), name='order-detail'),
    path('create/', OrderCreateView.as_view(), name='create-order'),
    path('by-master/', OrderMasterListView.as_view(), name='orders-master-list'),
]
