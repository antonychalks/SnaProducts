from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client

from checkout.models import Order
from .models import UserProfile


# Create your tests here.
class TestProfileViews(TestCase):
    def setUp(self):
        self.client = Client()

    def create_user_and_profile(self):
        self.user = User.objects.create_user(username="TestUser",
                                             email="<EMAIL>",
                                             password="<PASSWORD>")

    def test_profile_view_GET(self):
        self.create_user_and_profile()

        self.client.login(username='TestUser', password='<PASSWORD>')

        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)

    def test_profile_view_POST_form_valid(self):
        self.create_user_and_profile()

        self.client.login(username='TestUser', password='<PASSWORD>')

        response = self.client.post(reverse('profile'), data={
            'default_phone_number': '123456789',
            'default_first_line_address': 'Test Address 1',
            'default_second_line_address': 'Test Address 2',
            'default_town_or_city': 'Test City',
            'default_county': 'Test County',
            'default_postcode': 'Test Postcode',
            'default_country': 'Test Country',
        })

        self.assertEqual(response.status_code, 200)

    def test_order_history_GET(self):
        self.create_user_and_profile()

        # Create a test order
        order = Order.objects.create(full_name='Test',
                                     phone_number='123456789',
                                     country='Test Country',
                                     postcode='Test Postcode',
                                     town_or_city='Test City',
                                     first_line_address='Test Address',
                                     second_line_address='Test Address',
                                     county='Test County',)

        self.client.login(username='TestUser', password='<PASSWORD>')

        response = self.client.get(reverse('order_history', args=[order.order_number]))

        self.assertEqual(response.status_code, 200)


        self.client.login(username='Test', password='password')

        response = self.client.get(reverse('order_history', args=[order.order_number]))

        self.assertEqual(response.status_code, 200)


