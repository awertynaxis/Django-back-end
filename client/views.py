from django.db.models import Model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response

from client.models import Client
from client.serializers import CategorySerializer, ClientSerializer, ClientEditSerializer
from master.models import Category, Master
from master.serializers import MasterSerializer


class CategoriesListView(generics.ListCreateAPIView):
    """Gives a list of categories."""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class MastersByCategoriesView(APIView):
    """Gives a list of IDs and nicknames of masters who provide services in the selected `category`."""
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
    """Gives a list of clients and their info."""
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    # TODO: is this necessary?
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['master__master_telegram_id', 'client_telegram_id']


class ClientRegisterView(mixins.CreateModelMixin, generics.GenericAPIView):
    """Registers client in the database. Used when bot receives a `/start` command."""
    serializer_class = ClientSerializer

    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        serializer.is_valid()
        # `get_or_create` method returns a tuple, hence why 2 variables are used
        # this method calls a `get` method with keyword arguments provided in this function call,
        # checks whether this DB entry exists and if not it creates one,
        # preventing creation of duplicate client DB entries
        obj, created = Client.objects.get_or_create(client_telegram_id=request.data['client_telegram_id'],
                                                    client_telegram_nickname=request.data['client_telegram_nickname'],
                                                    defaults=serializer.validated_data)
        if created:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_409_CONFLICT)

    # TODO: PATCH request when user registers properly (sends their TG contact to the bot)


# TODO: remove from release version?
class ClientDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """Gives detailed info of a specified client.
    Used for debug purposes only."""
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


# TODO: move this to `master` app?
class ClientMasterGetID(APIView):
    """Gives ID of a master with a specified nickname. Receives a {"nickname": '____'} JSON as a request."""
    def get(self, request):
        master_nickname = request.data['nickname']
        try:
            master = Master.objects.get(nickname=master_nickname)
        # returns an empty JSON in case no matching master is found
        except Model.DoesNotExist:
            return Response({})
        id = MasterSerializer(master).data['id']
        return Response(id)


# TODO: merge with ClientDetailsView?
class ClientMasterEditView(APIView):
    """Edits client's info. Used when client edits their list of saved masters."""
    def get_object(self, telegram_id):
        return Client.objects.get(client_telegram_id=telegram_id)

    # implementing GET request handler for easier web API view experience
    def get(self, request, telegram_id):
        client = self.get_object(telegram_id)
        return Response(ClientEditSerializer(client).data)

    def patch(self, request, telegram_id):
        """Can be used for both adding and deleting masters from user's list of saved masters."""
        client = self.get_object(telegram_id)
        # bot sends a JSON with all data about the user (stored in `request`), including
        # new masters list, hence why `data` argument is used
        client_data = ClientEditSerializer(client, data=request.data)
        if client_data.is_valid():
            client_data.save()
            return Response(client_data.data)
        return Response(client_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientMasterListView(APIView):
    """Gets a list of ID's and nicknames of masters that a specified (by `telegram_id`) client has."""
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
