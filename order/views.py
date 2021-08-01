from datetime import timedelta
from django.utils.dateparse import parse_datetime
from rest_framework import generics, status
from rest_framework.response import Response

from client.models import Client
from order.models import Order
from order.serializers import OrderSerializer, CreateOrderSerializer, OrderForMasterSerializer
from order.filters import OrderClientFilter, OrderMasterFilter
from schedule.models import Schedule


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
    """Creates an order and ties it to corresponding schedule slots."""
    model = Order
    serializer_class = CreateOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """Gets an internal ID of the Telegram user making the order, adds it to the order entry and saves the entry."""
        client_telegram_id = self.request.data['client_telegram_id']
        client = Client.objects.get(client_telegram_id=client_telegram_id)
        serializer.save(client=client)
        self.schedule_update(serializer.data['id'])

    def schedule_update(self, order):
        """Updates corresponding schedule slots with the order booked on these slots."""
        # all these fields are present in a JSON sent to the endpoint
        duration = self.request.data['duration']
        master = self.request.data['master']
        start_slot = parse_datetime(self.request.data['start_datetime_slot'])

        # creating a list of all slots corresponding to the order
        slots = [
            Schedule.objects.get(master_id=master,
                                 # corresponding timeslots are calculated by taking the timestamp of the beginning
                                 # of the order and adding an offset (as we iterate through `for` condition below)
                                 # result datetime object is turned back into a str as get() method accepts strings only
                                 # TODO: will this work with timezones other than UTC+0?
                                 datetime_slot=(start_slot + timedelta(hours=offset)).strftime("%Y-%m-%dT%H:%M:%SZ"))
            for offset in range(duration)
        ]
        # editing `order` fields of each corresponding slot
        for slot in slots:
            slot.order_id = order
        # bulk_update() lets us update all corresponding slots at once
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
