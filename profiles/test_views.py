from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client

from checkout.models import Order
from .models import UserProfile


# Create your tests here.
class TestProfileViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="Test user", email="<EMAIL>", password="<PASSWORD>")
        self.user.save()

        self.UserProfile = UserProfile.objects.create(user=self.user, default_phone_number="07747474743",
                                                      default_first_line_address="first_line_address",
                                                      default_second_line_address="second_line_address",
                                                      default_town_or_city="town_or_city",
                                                      default_postcode="post_code",
                                                      default_county="county", default_country="country")
        self.UserProfile.save()

    def test_profile_view_GET(self):
        self.client.login(username='Test', password='password')

        response = self.client.get(reverse('profile'))

        self.assertEquals(response.status_code, 200)

    def test_order_history_GET(self):
        # Create a test order
        order = Order.objects.create(full_name='Test', phone_number='123456789',
                                     country='Test Country',
                                     post_code='Test Postcode',
                                     town_or_city='Test City',
                                     street_address1='Test Address')

        self.client.login(username='Test', password='password')

        response = self.client.get(reverse('order_history', args=[order.id]))

        self.assertEquals(response.status_code, 200)


