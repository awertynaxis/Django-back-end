import random
import requests
from django.test import TestCase
from django.urls import reverse
from Django_backend.factories import ClientFactory, CategoryFactory, UserFactory, MasterFactory, ServiceFactory
from faker import Factory
from faker import Faker
from client.models import Client
from master.models import Master, Service

faker = Factory.create()
super_fake = Faker()




class ClientFactoryTest(TestCase):
    def test_get_existing_client(self):
        client = ClientFactory()

        expected_status_code = 200
        expected_client_count = 1

        response = self.client.get(reverse('client-list'),
                                   data={'client_telegram_id': client.client_telegram_id})

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_client_count, len(response.json()))

    def test_create_test_category(self):
        CategoryFactory.create_batch(5, category_name=faker.word())

        expected_status_code = 200
        expected_category_count = 5

        response = self.client.get(reverse('categories'))

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_category_count, len(response.json()))

    def test_get_categoris_by_master(self):

        expected_status_code = 200
        expected_client_count = 1
        user = UserFactory()
        master = MasterFactory(user=user)
        category = CategoryFactory()

        service = ServiceFactory(master=master, category=category)

        response = self.client.get(f'http://127.0.0.1:8000/client/categories/{category.id}')

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_client_count, Master.objects.filter(services__category=category).count())

    def test_detail_client_info(self):

        expected_status_code = 200
        expected_client_count = 1

        for clients in range(4):
            client_telegram_id = random.randint(100000000, 100000000000000)
            client = ClientFactory(client_telegram_id=client_telegram_id)
            response = self.client.get(f'http://127.0.0.1:8000/client/clients/{client.id}')

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_client_count, Client.objects.filter(pk=3).count())

    def test_create_client_master_list(self):

        expected_status_code = 301
        expected_client_count = 3
        # user_1 = UserFactory(username='dodo')
        # master_1 = MasterFactory(user=user_1, nickname='kol')
        # user_2 = UserFactory(username='mikle')
        # master_2 = MasterFactory(user=user_2)
        # user_3 = UserFactory(username='shol')
        # master_3 = MasterFactory(user=user_3, nickname='lol')

        user_list = UserFactory.create_batch(3)
        master_list=[]
        for user in user_list:
            master = MasterFactory(user=user)
            master_list.append(master.id)

        # user = UserFactory.create_batch(3, username = faker.name())

        # user = UserFactory.create_batch(3)
        # client = ClientFactory.create(master=(master))
        client = ClientFactory()
        client.master.add(1, 2, 3)

        response_master_list = self.client.get(f'http://127.0.0.1:8000/client/clients/master_list/{client.client_telegram_id}')

        self.assertEqual(expected_status_code, response_master_list.status_code)
        self.assertEqual(expected_client_count, Master.objects.filter(clients__client_telegram_id=client.client_telegram_id).count())

        added_new_user = UserFactory()
        added_new_master = MasterFactory(user=added_new_user)
        master_list.append(added_new_master.id)

        response_add_master = self.client.put(f'http://127.0.0.1:8000/client/clients/add_master/{client.client_telegram_id}',
                                              data={'client_telegram_id': client.client_telegram_id,
                                                    'client_telegram_nickname': client.client_telegram_nickname,
                                                    'client_phone_number': client.client_phone_number,
                                                    'master': master_list
                                                    }, content_type='application/json')

        expected_new_client_count = 4
        expected_new_status_code = 200
        self.assertEqual(expected_new_status_code, response_add_master.status_code)
        self.assertEqual(expected_new_client_count,
                         Master.objects.filter(clients__client_telegram_id=client.client_telegram_id).count())

    def test_get_master_id(self):

        expected_status_code = 200
        expected_master_count = 1

        user = UserFactory()
        master = MasterFactory(user=user)
        url = 'http://127.0.0.1:8000/client/clients/add_master/get_id/'
        response = requests.get(url, json={'nickname': master.nickname})

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_master_count, Master.objects.filter(nickname=master.nickname).count())


# Create your tests here.
