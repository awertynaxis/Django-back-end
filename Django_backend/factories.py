import random
import uuid

import factory
from django.contrib.auth.models import User

from master.models import Master, Service, Category, VerifyCodes
from client.models import Client
from faker import Factory
from faker import Faker

from order.models import Order
from schedule.models import Schedule

super_fake = Faker()
faker = Factory.create()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    category_name = faker.word()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    first_name = faker.name()
    username = factory.LazyFunction(faker.name)
    # username = faker.name()  #faker.name() / super_fake.unique.name()
    password = faker.password()


class MasterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Master

    nickname = factory.LazyFunction(faker.name)
    user = factory.SubFactory(UserFactory)


class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Service

    title = faker.name()
    duration = 1
    price = faker.word()
    description = faker.text()
    category = factory.SubFactory(CategoryFactory)
    master = factory.SubFactory(MasterFactory)


class VerifyCodesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VerifyCodes

    code = str(uuid.uuid4())
    master = factory.SubFactory(MasterFactory)


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client

    client_telegram_id = factory.LazyFunction(faker.pyint)
    client_telegram_nickname = faker.word()
    client_phone_number = faker.word()

    # @factory.post_generation
    # def master(self, create, extracted, **kwargs):
    #     if not create:
    #         if not create:
    #             return
    #     if extracted:
    #         for masters in extracted:
    #             self.master.add(masters)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    master = factory.SubFactory(MasterFactory)
    client = factory.SubFactory(ClientFactory)
    service = factory.SubFactory(ServiceFactory)


class ScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Schedule

    master = factory.SubFactory(MasterFactory)
    order = factory.SubFactory(OrderFactory)
    datetime_slot = faker.date_time()
