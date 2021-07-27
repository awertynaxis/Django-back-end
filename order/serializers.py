from rest_framework import serializers

from order.models import Order
from master.models import Service, Master
from client.models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('client_telegram_id', 'client_telegram_nickname')


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('title', 'price')


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = ('nickname', 'id')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'service', 'master')
        read_only_field = ('id',)
        depth = 1
    service = ServiceSerializer()
    master = MasterSerializer()


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_field = ('id', )


class ServiceMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('title', 'price','duration')


class OrderForMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_field = ('id', )
        depth = 1
    client = ClientSerializer()
    service = ServiceMasterSerializer()
    master = MasterSerializer()
