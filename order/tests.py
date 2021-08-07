import dataclasses
import datetime
import random
from typing import List

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from order.models import Order
from client.models import Client
from master.models import Master, Service, Category
from schedule.models import Schedule


@dataclasses.dataclass
class CreatingTestObject:

    username: str = 'coconut'
    password: str = 'room44'
    nickname: str = 'coconut'
    client_telegram_id: int = 700993894
    client_telegram_nickname: str = 'testcoconut'
    client_phone_number: str = '+375291170940'
    category_name: str = 'nails'
    duration: int = 1
    title: str = 'french'
    list_of_service: List[str] = dataclasses.field(default_factory=['nails', 'french', 'pedikure', 'growing up'])

    @staticmethod
    def create_test_master(username=username, password=password, nickname=nickname):
        user = User.objects.create(username=username, password=password)
        master = Master.objects.create(nickname=nickname, user_id=user.id)
        return master

    @staticmethod
    def create_test_client(client_telegram_id=client_telegram_id):
        client = Client.objects.create(client_telegram_id=client_telegram_id)
        return client

    @staticmethod
    def create_test_category(category_name=category_name):
        category = Category.objects.create(category_name=category_name)
        return category

    @staticmethod
    def create_test_service(master_id, category_id, duration=duration, title=title):
        service = Service.objects.create(title=title,
                                         master_id=master_id,
                                         category_id=category_id,
                                         duration=duration)
        return service

    @staticmethod
    def create_test_order(client_id, master_id, service_id):
        order = Order.objects.create(client_id=client_id,
                                     master_id=master_id,
                                     service_id=service_id)
        return order


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

        response = self.client.get(reverse('client-list'),
                                   data={'client_telegram_id': client.client_telegram_id})

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_client_count, len(response.json()))


class MasterSkillTestCase(TestCase, CreatingTestObject):
    def test_get_master_skills(self):
        master_a = CreatingTestObject.create_test_master(username='Grisha', password='Shrek767', nickname='Gringo')
        master_b = CreatingTestObject.create_test_master()
        category = CreatingTestObject.create_test_category(category_name='brows')
        list_of_service = ['nails', 'french', 'pedikure', 'growing up']
        for service in list_of_service:
            CreatingTestObject.create_test_service(title=service,
                                                   master_id=master_a.id,
                                                   category_id=category.id,
                                                   )
            CreatingTestObject.create_test_service(title=service,
                                                   master_id=master_b.id,
                                                   category_id=category.id,
                                                   duration=random.randint(1, 10)
                                                   )

        expected_status_code = 200
        expected_master_count_skill = 4
        expected_masters_skills = 8

        response_master_skills = self.client.get(reverse('skill_list'), data={'nickname': master_b.nickname})

        response_all_masters_skills = self.client.get(reverse('skill_list'))
        self.assertEqual(expected_status_code, response_master_skills.status_code)
        # self.assertEqual(expected_master_count_skill, len(response_master_skills.json()))
        self.assertEqual(expected_masters_skills, len(response_all_masters_skills.json()))


class OrderTestCase(TestCase, CreatingTestObject):
    def test_get_filtered_order(self):
        list_of_objects = CreatingTestObject.create_test_objects()
        Order.objects.create(client_id=list_of_objects[2].id,
                             master_id=list_of_objects[1].id,
                             service_id=list_of_objects[4].id)
        master = CreatingTestObject.create_test_master('algima', 'sey4asbudu25','algima')
        client = CreatingTestObject.create_test_client(client_telegram_id=345678094)
        category = CreatingTestObject.create_test_category(category_name='nails')
        service = CreatingTestObject.create_test_service(category_id=category.id,
                                                         master_id=master.id,
                                                         title=CreatingTestObject.title,
                                                         duration=CreatingTestObject.duration
                                                         )
        for x in range(5):
            CreatingTestObject.create_test_order(client_id=client.id,
                                                 master_id=master.id,
                                                 service_id=service.id
                                                 )
        expected_status_code = 200
        expected_order_count = 5

        response = self.client.get(reverse('order-list'),
                                   data={'client_telegram_id': client.client_telegram_id}
                                   )

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_order_count, len(response.json()))

    def test_get_master_order_list(self):
        list_of_objects = CreatingTestObject.create_test_objects()
        master = CreatingTestObject.create_test_master()
        client = CreatingTestObject.create_test_client()
        for maker_order in range(2):
            Order.objects.create(client_id=list_of_objects[2].id,
                                 master_id=list_of_objects[1].id,
                                 service_id=list_of_objects[4].id)
            Order.objects.create(client_id=client.id,
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
        client = CreatingTestObject.create_test_client()
        master = CreatingTestObject.create_test_master(username='Anton', password='Bugabiba', nickname='awerty_naxis')
        category = CreatingTestObject.create_test_category()
        service = CreatingTestObject.create_test_service(master_id=master.id,
                                                         category_id=category.id
                                                         )
        schedule = Schedule.objects.create(master=master, datetime_slot=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
        response = self.client.post(reverse('create-order'), data={
                'client_telegram_id': client.client_telegram_id,
                'master': master.id,
                'service': service.id,
                'start_datetime_slot': schedule.datetime_slot
            }, content_type='application/json')

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_make_count, Order.objects.count())

    def test_delete_order(self):
        expected_status_code = 200
        expected_order_count = 0

        # Existing order needed
        list_of_objects = CreatingTestObject.create_test_objects()
        order = Order.objects.create(client_id=list_of_objects[2].id,
                                     master_id=list_of_objects[1].id,
                                     service_id=list_of_objects[4].id)
        response = self.client.delete(reverse('order-detail', args=[order.pk]))

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_order_count, Order.objects.count())
