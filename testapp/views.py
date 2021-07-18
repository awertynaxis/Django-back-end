from django.shortcuts import render
from rest_framework import generics
from .models import AddedMasters
from .serializers import AddedMastersSerializer
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
# 443993822
# 443993822
class AddedMastersList(generics.ListCreateAPIView):
      lookup_field = 'pk'
      serializer_class = AddedMastersSerializer
      queryset = AddedMasters.objects.filter(client__telegram_id='pk')




class AddedMastersDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddedMastersSerializer
    queryset = AddedMasters.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client_id']


list_added_masters_view = AddedMastersList.as_view()
details_added_masters_view = AddedMastersDetails.as_view()
