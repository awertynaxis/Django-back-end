from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from client.models import Client
from client.serializers import ClientSerializer


class ClientView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['master__master_telegram_id', 'client_telegram_id']


# TODO: maybe??
class ClientDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class ClientMasterListView(APIView):

    def get_object(self, pk):
        return Client.objects.get(pk=pk)

    def get(self, request, pk):
        client = self.get_object(pk)
        masters_data = ClientSerializer(client).data['master']
        # stuff = serializer.data['master']

        # TODO: try to implement filter here
        result_set = [
            {
                "id": master['id'],
                "nickname": master['nickname']
            }
            for master in masters_data
        ]
        return Response(result_set)


list_client_view = ClientView.as_view()
details_client_view = ClientDetailsView.as_view()
