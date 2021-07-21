from rest_framework import serializers

from client.models import Client
from master.models import Master


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_field = ('id',)


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = '__all__'
        read_only_field = ('id',)
