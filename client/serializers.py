from rest_framework import serializers

from client.models import Client
from master.models import Category


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_field = ('id',)
        # necessary for ClientMasterListView data parsing
        depth = 1


class ClientEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_field = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_field = ('id',)
