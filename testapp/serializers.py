from rest_framework import serializers

from .models import Master, Client, AddedMasters


class AddedMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddedMasters
        fields = ('id', 'client', 'master',)
        read_only_fields = ('id',)
