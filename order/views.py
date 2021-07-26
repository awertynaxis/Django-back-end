from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import Order
from order.serializers import OrderSerializer, CreateOrderSerializer, OrderForMasterSerializer
from order.filters import OrderClientFilter, OrderMasterFilter


class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filterset_class = OrderClientFilter


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderCreateView(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer
    queryset = Order.objects.all()


class OrderMasterListView(generics.ListAPIView):
    serializer_class = OrderForMasterSerializer
    queryset = Order.objects.all()
    filterset_class = OrderMasterFilter


list_order_view = OrderListView.as_view()
detail_order_view = OrderDetailView.as_view()
create_order_view = OrderCreateView.as_view()
list_order_master_view = OrderMasterListView.as_view()
# Create your views here.
