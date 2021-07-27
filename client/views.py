from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from client.models import Client
from client.serializers import CategorySerializer, ClientSerializer, ClientEditSerializer
from master.models import Category, Master
from master.serializers import MasterSerializer


class CategoriesListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class MastersByCategoriesView(APIView):
    def get_masters(self, category):
        # getting entries of all masters who provide services
        # that belong in the requested category
        return Master.objects.filter(services__category=category)

    def get(self, request, category):
        masters = self.get_masters(category)
        # needs `many=True` in serializer parameters to work
        serialized_masters = MasterSerializer(masters, many=True).data

        if not serialized_masters:
            return Response(status.HTTP_204_NO_CONTENT)

        # removing duplicate masters data using frozenset
        # via assigning a value to key as a frozenset
        masters_data = {
            frozenset(item.items()): item
            for item in serialized_masters
        }.values()

        # TODO: try to implement filter here
        result_list = masters_data_trimmer(masters_data)
        return Response(result_list)


class ClientView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['master__master_telegram_id', 'client_telegram_id']


class ClientRegisterView(generics.CreateAPIView):
    serializer_class = ClientSerializer


# TODO: maybe??
class ClientDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class ClientMasterGetID(APIView):
    def get(self, request):
        master_nickname = request.data['nickname']
        try:
            master = Master.objects.get(nickname=master_nickname)
        # returns an empty JSON in case no matching master is found
        except:
            return Response({})
        id = MasterSerializer(master).data['id']
        return Response(id)


class ClientMasterEditView(APIView):
    def get_object(self, telegram_id):
        return Client.objects.get(client_telegram_id=telegram_id)

    # implementing GET request handler for easier web API view experience
    def get(self, request, telegram_id):
        client = self.get_object(telegram_id)
        return Response(ClientEditSerializer(client).data)

    def put(self, request, telegram_id):
        client = self.get_object(telegram_id)
        # bot sends a JSON with all data about the user, including
        # new masters list, hence why `data` argument is used
        client_data = ClientEditSerializer(client, data=request.data)
        if client_data.is_valid():
            client_data.save()
            return Response(client_data.data)
        return Response(client_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientMasterListView(APIView):
    def get_object(self, telegram_id):
        return Client.objects.get(client_telegram_id=telegram_id)

    def get(self, request, telegram_id):
        client = self.get_object(telegram_id)
        masters_data = ClientSerializer(client).data['master']

        if not masters_data:
            return Response(status.HTTP_204_NO_CONTENT)

        # TODO: try to implement filter here
        result_list = masters_data_trimmer(masters_data)
        return Response(result_list)


def masters_data_trimmer(masters_data):
    """Auxiliary function for trimming data about a master to two fields."""
    return [
            {
                "id": master['id'],
                "nickname": master['nickname']
            }
            for master in masters_data
        ]


list_client_view = ClientView.as_view()
details_client_view = ClientDetailsView.as_view()
