import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from client.models import Client
from master.models import Master, Service, Category, VerifyCodes
from Django_backend.factories import CategoryFactory, ClientFactory, UserFactory, MasterFactory, ServiceFactory, \
    VerifyCodesFactory

from faker import Factory
faker = Factory.create()
# User = get_user_model()


class MasterFactoryTests(TestCase):

    def test_create_master_skills(self):
        user = UserFactory()
        master = MasterFactory(user=user)
        category = CategoryFactory()
        ServiceFactory.create_batch(5, master=master, category=category)
        expected_master_count = 1

        expected_status_code = 200
        expected_master_count_skill = 5

        response_master_skills = self.client.get(reverse('skill_list'),
                                                 data={'nickname': master.nickname})

        self.assertEqual(expected_status_code, response_master_skills.status_code)
        self.assertEqual(expected_master_count_skill, len(response_master_skills.json()))

        self.assertEqual(expected_master_count, Master.objects.filter(pk=master.id).count())

    def test_create_verify_codes(self):

        expected_code_count = 1
        user = UserFactory()
        master = MasterFactory(user=user)
        verify_code = VerifyCodesFactory(master=master)

        self.assertEqual(expected_code_count, VerifyCodes.objects.filter(pk=verify_code.id).count())

    def test_create_add_master_telegram_info(self):
        expected_status_code = 200
        user = UserFactory()
        master = MasterFactory(user=user)
        verify_code = VerifyCodesFactory(master=master)
        master_telegram_id = str(random.randint(100000000, 1000000000000000))
        master_telegram_nickname = faker.name()

        response = self.client.put(reverse('add_master_telegram'), data={
                    'verify_code': verify_code.code,
                    'master_telegram_id': master_telegram_id,
                    'master_telegram_nickname': master_telegram_nickname

                }, content_type='application/json')
        self.assertEqual(expected_status_code, response.status_code)
        self.assertTrue(Master.objects.filter(master_telegram_id=master_telegram_id,
                                              master_telegram_nickname=master_telegram_nickname))

    # def test_create_user(self):
    #
    #     user = User.objects.create_user(username='blabla', password='Gopa123gopa', email='jsgovno@mail.ru')
    #     response = self.client.post(reverse('signupuser'), data={
    #             'username': user,
    #             'password1': password_1,
    #             'password2': password_2
    #         }, content_type='application/json')
    #
    #     expected_master_count = 1
    #     self.assertEqual(expected_master_count, User.objects.filter(username=user).count())

    # def test_create_master(self):
    #     expected_status_code = 201
    #     expected_status_code = 200
    #     expected_master_count = 1
    #
    #     user = User.objects.create_user(username='blabla', password='Gopa123gopa',email='jsgovno@mail.ru',)
    #     user.save()
    #     user = UserFactory()
    #     master = MasterFactory(user=user)
    #     master = Master.objects.create(nickname='zal', user_id=user.id)
    #     response_a = self.client.post('signup/', {'username': 'blabla',
    #     'password': 'Gopa123gopa', 'nickname': 'gora'})
    #     response_b = self.client.post('login/', {'username':'blabla','password':'Gopa123gopa', 'nickname':'gora'})
    #
    #     self.assertEqual(expected_status_code, response_b.status_code)
    #     self.assertEqual(expected_master_count, User.objects.count())

    # def test_create_service(self):
    #     expected_status_code = 201
    #     expected_make_count = 1
    #     user = UserFactory()
    #     master = MasterFactory(user=user)
    #     category = CategoryFactory()
    #
    #
    #     response = self.client.post(reverse('add_service'), data={
    #             'user' : user.id,
    #             'price': '25$',
    #             'master': master.id,
    #             'category': category.id,
    #             'title': faker.word(),
    #             'duration': 2,
    #         }, content_type='application/json')
    #     self.assertEqual(expected_status_code, response.status_code)
    #     self.assertEqual(expected_make_count, Service.objects.count())
# Create your tests here.
