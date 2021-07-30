from order.models import Order
from django_filters import rest_framework as filters


class OrderClientFilter(filters.FilterSet):
    client_telegram_id = filters.CharFilter(field_name='client__client_telegram_id', lookup_expr='exact')

    class Meta:
        model = Order
        fields = ['client_telegram_id']


class OrderMasterFilter(filters.FilterSet):
    nickname = filters.CharFilter(field_name='master__nickname', lookup_expr='exact')

    class Meta:
        model = Order
        fields = ['nickname']
