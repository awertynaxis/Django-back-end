from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
from rest_framework import generics, status
from rest_framework.response import Response

from client.models import Client
from order.models import Order
from order.serializers import OrderSerializer, CreateOrderSerializer, OrderForMasterSerializer
from order.filters import OrderClientFilter, OrderMasterFilter
from schedule.models import Schedule
from schedule.serializers import ScheduleSerializer


class OrderListView(generics.ListCreateAPIView):
    """Gives a list of all orders.
    Implemented for debug purposes and isn't used by any client."""
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filterset_class = OrderClientFilter


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Gives detailed info of a specified order."""
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderCreateView(generics.CreateAPIView):
    """Creates an order."""
    model = Order
    serializer_class = CreateOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        client_telegram_id = self.request.data['client_telegram_id']
        client = Client.objects.get(client_telegram_id=client_telegram_id)
        serializer.save(client=client)
        self.schedule_update(serializer.data['id'])

    def schedule_update(self, order):
        duration = self.request.data['duration']
        master = self.request.data['master']
        start_slot = parse_datetime(self.request.data['start_datetime_slot'])

        # for offset in range(duration):
        #     # get schedule slot; with each iteration of offset, we gain 1 hour
        #     # edit current slot's order ID
        #     # save slot
        #     pass

        slots = [
            Schedule.objects.get(master_id=master,
                                 datetime_slot=(start_slot + timedelta(hours=offset)).strftime("%Y-%m-%dT%H:%M:%SZ"))
            for offset in range(duration)
        ]
        for slot in slots:
            slot.order_id = order
        Schedule.objects.bulk_update(slots, ['order_id'])


class OrderMasterListView(generics.ListAPIView):
    """Gives a list of all orders associated with a specified master."""
    serializer_class = OrderForMasterSerializer
    queryset = Order.objects.all()
    filterset_class = OrderMasterFilter


# TODO: remove this and use ViewName.as_view() in urls.py?
# list_order_view = OrderListView.as_view()
# detail_order_view = OrderDetailView.as_view()
# create_order_view = OrderCreateView.as_view()
# list_order_master_view = OrderMasterListView.as_view()
