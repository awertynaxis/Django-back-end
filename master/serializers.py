from rest_framework import serializers
from master.models import Master, Service


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = '__all__'
        read_only_field = ('id',)


class MasterSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'title',)
        read_only_field = ('id',)


class DetailSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        read_only_field = ('id',)


class AddServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = ('master',)
        read_only_field = ('id',)


class CreateMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        exclude = ('user', 'master_telegram_id', 'master_telegram_nickname',)
        read_only_field = ('id',)


class AddMasterTelegramInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = ('master_telegram_id', 'master_telegram_nickname')
        read_only_field = ('id',)
