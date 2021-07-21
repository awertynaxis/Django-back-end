from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .models import Client, Master
from .serializers import ClientSerializer, MasterSerializer
# Create your views here.


class ClientView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['master__master_telegram_id', 'client_telegram_id']


class MasterView(generics.ListCreateAPIView):
    serializer_class = MasterSerializer
    queryset = Master.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['clients__client_telegram_id']


list_client_view = ClientView.as_view()
list_master_view = MasterView.as_view()

