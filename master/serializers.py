from rest_framework import serializers
from master.models import Master, Service


class MasterSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'title', 'master')
        read_only_field = ('id',)


class DetailSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        read_only_field = ('id',)


class AddServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        read_only_field = ('id')