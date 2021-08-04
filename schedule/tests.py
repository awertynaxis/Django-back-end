from django.test import TestCase
from Django_backend.factories import UserFactory, MasterFactory, CategoryFactory, \
    ClientFactory, ServiceFactory, ServiceFactory, OrderFactory, ScheduleFactory
from faker import Factory
from faker import Faker

from schedule.models import Schedule

faker = Factory.create()
super_fake = Faker()


class ScheduleFactoryTest(TestCase):

    def test_get_existing_client(self):

        expected_status_code = 301
        expected_client_count = 1
        user = UserFactory()
        master = MasterFactory(user=user)

        category = CategoryFactory()
        service = ServiceFactory(master=master, category=category)

        client = ClientFactory()
        order = OrderFactory(client=client, master=master, service=service)
        schedule = ScheduleFactory(order=order, master=master)

        response = self.client.get(f'http://127.0.0.1:8000/schedule')

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_client_count, Schedule.objects.all().count())

# Create your tests here.
