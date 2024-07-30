import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from profiles.models import UserProfile
from products.models import Product, Category
from .models import Order, OrderLineItem


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.checkout_url = reverse('checkout')

        # Set up necessary test data

        self.user = User.objects.create_user(
            username='testuser',
            email='test@user.com',
            password='testpass123'
        )

        self.profile, created = UserProfile.objects.get_or_create(
            user=self.user,
            defaults={
                'default_phone_number': '123456789',
                'default_country': 'Country Name',
                'default_postcode': '12345',
                'default_town_or_city': 'City Name',
                'default_first_line_address': 'Address Line 1',
                'default_second_line_address': 'Address Line 2',
                'default_county': 'County Name'
            }
        )

        self.category = Category.objects.create(
            name="Miscellaneous"
        )

        self.product = Product(
            id="9999",
            category=self.category,
            sku="TEST9999",
            name="test product",
            description="test description",
            price=99.99,
            rating="3"
        )

        self.product.save()

        self.order = Order.objects.create(
            user_profile=self.profile,
            full_name='First Name',
            email='test@user.com',
            phone_number='1234567890',
            country='Country Name',
            first_line_address='Address Line 1',
            second_line_address='Address Line 2',
            town_or_city='City Name',
            postcode='12345',
            county='County Name',
            original_cart=json.dumps({}),
            stripe_pid='stripepid',
        )

        self.order.save()

        OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
        )
        self.client.login(username='testuser', password='testpass123')

        session = self.client.session
        session['cart'] = {str(self.product.id): 1}
        session.save()

    def test_GET_checkout(self):
        response = self.client.get(self.checkout_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_GET_checkout_success(self):
        order = Order.objects.get(email='test@user.com')
        checkout_success_url = reverse('checkout_success', args=[order.order_number])
        response = self.client.get(checkout_success_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')

    def test_checkout_with_empty_cart(self):
        session = self.client.session
        session['cart'] = {}
        session.save()

        response = self.client.get(self.checkout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('products'))
