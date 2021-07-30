from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from order.models import Order
from client.models import Client
from master.models import Master, Service, Category


class CreatingTestObject:

    @staticmethod
    def create_test_objects():
        user = User.objects.create(username='kvakva', password='sickbrain2552')
        master = Master.objects.create(nickname='ashly', user_id=user.id)
        client = Client.objects.create(client_telegram_id=543993894,
                                       client_telegram_nickname='testdude',
                                       client_phone_number='+375447655059')
        category = Category.objects.create(category_name='nails for woman')
        service = Service.objects.create(title='nails',
                                         master_id=master.id,
                                         category_id=category.id,
                                         duration=3)

        return [user, master, client, category, service]


class ClientTestCase(TestCase, CreatingTestObject):
    def test_get_existing_client(self):

        client = CreatingTestObject.create_test_objects()[2]
        expected_status_code = 200
        expected_client_count = 1

        response = self.client.get(reverse('client-list'))

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_client_count, len(response.json()))

        return client


class MasterTestCase(TestCase, CreatingTestObject):
    def test_get_existing_master(self):
        CreatingTestObject.create_test_objects()[1]
        expected_status_code = 200
        expected_master_count = 1

        response = self.client.get(reverse('master-list'))

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_master_count, len(response.json()))


class OrderTestCase(TestCase, CreatingTestObject):
    def test_get_filtered_order(self):
        list_of_objects = CreatingTestObject.create_test_objects()
        Order.objects.create(client_id=list_of_objects[2].id,
                             master_id=list_of_objects[1].id,
                             service_id=list_of_objects[4].id)
        expected_status_code = 200
        expected_order_count = 1

        response = self.client.get(reverse('order-list'),
                                   data={'client_telegram_id': list_of_objects[2].client_telegram_id}
                                   )

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_order_count, len(response.json()))

    def test_get_master_orderlist(self):
        list_of_objects = CreatingTestObject.create_test_objects()
        for maker_order in range(2):
            Order.objects.create(client_id=list_of_objects[2].id,
                                 master_id=list_of_objects[1].id,
                                 service_id=list_of_objects[4].id)
        user = User.objects.create(username='test', password='sickbrainio2552')
        master = Master.objects.create(nickname='testy', user_id=user.id)
        Order.objects.create(client_id=list_of_objects[2].id,
                             master_id=master.id,
                             service_id=list_of_objects[4].id)
        expected_status_code = 200
        expected_order_count = 2

        response = self.client.get(reverse('orders-master-list'),
                                   data={'nickname': list_of_objects[1].nickname}
                                   )
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_order_count, len(response.json()))
        self.assertEqual(expected_order_count, Order.objects.filter(master_id=list_of_objects[1].id).count())

    def test_create_new_order(self):

        expected_status_code = 201
        expected_make_count = 1
        list_of_objects = CreatingTestObject.create_test_objects()
        response = self.client.post(reverse('create-order'), data={
                'client': list_of_objects[2].id,
                'master': list_of_objects[1].id,
                'service': list_of_objects[4].id
            }, content_type='application/json')

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_make_count, Order.objects.count())

    def test_delete_order(self):
        expected_status_code = 204
        expected_order_count = 0

        # Existing order needed
        list_of_objects = CreatingTestObject.create_test_objects()
        order = Order.objects.create(client_id=list_of_objects[2].id,
                                     master_id=list_of_objects[1].id,
                                     service_id=list_of_objects[4].id)
        response = self.client.delete(reverse('order-detail', args=[order.pk]))

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_order_count, Order.objects.count())
