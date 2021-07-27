from django.urls import re_path, path

from order.views import list_order_view, detail_order_view, create_order_view, list_order_master_view

urlpatterns = [
    path('orders/', list_order_view, name='order-list'),
    re_path(r'^orders/(?P<pk>\d+)$', detail_order_view, name='order-detail'),
    path('order-create/', create_order_view, name='create-order'),
    path('master-orders/', list_order_master_view, name='orders-master-list'),
]