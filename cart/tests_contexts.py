from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from cart.contexts import cart_contents
from products.models import Product, Category


# Create your tests here.
class TestCartContent(TestCase):
    def setUp(self):
        # Create Product
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(id="9999", category=self.category, sku="TEST_SKU",
                                              name="Test Product", description="test description",
                                              price=99.99, rating=3)
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_empty_cart(self):
        # Test the content of an empty cart
        context = cart_contents(self.client)
        self.assertEqual(context['product_count'], 0)
        self.assertEqual(context['total'], 0)
        self.assertEqual(context['delivery'], 0)
        self.assertEqual(context['grand_total'], 0)
        self.assertEqual(context['cart_products'], [])

    def test_multiple_different_products(self):
        # Create a second product
        self.product_2 = Product.objects.create(id="9998", category=self.category,
                                                sku="TEST_SKU_2", name="Test Product 2",
                                                description="test description",
                                                price=75.99, rating=4)
        # Add the two test products to the cart
        session = self.client.session
        session['cart'] = {str(self.product.id): 1, str(self.product_2.id): 2}
        session.save()

        context = cart_contents(self.client)
        self.assertEqual(len(context['cart_products']), 2)
        self.assertEqual(context['product_count'], 3)
        self.assertEqual(context['total'], Decimal(str(1 * self.product.price)) + Decimal(
            str(2 * self.product_2.price)))
        self.assertEqual(context['grand_total'], context['total'] + context['delivery'])

    def add_sample_product_to_cart(self):
        # Define a function that adds a product to the cart for testing purposes
        session = self.client.session
        if 'cart' not in session:
            session['cart'] = {}
        session['cart'][str(self.product.id)] = 1
        session.save()

    def test_if_cart_products_are_added_correctly(self):
        self.add_sample_product_to_cart()

        context = cart_contents(self.client)
        self.assertTrue('cart_products' in context)
        self.assertEqual(len(context['cart_products']), 1)
        self.assertEqual(context['cart_products'][0]['product'], self.product)

    def test_delivery_and_total(self):
        # Test the content of the cart before adding an item
        context = cart_contents(self.client)
        self.assertEqual(context['total'], 0)
        self.assertEqual(context['delivery'], 0)

        # Add a test product to the cart
        self.add_sample_product_to_cart()

        # Test the content of the cart after adding an item
        context = cart_contents(self.client)
        min_half_delivery = context['min_half_delivery']
        min_free_delivery = context['min_free_delivery']

        if context['total'] < min_half_delivery:
            self.assertEqual(context['delivery'], context['total'] * settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        elif context['total'] < min_free_delivery:
            self.assertEqual(context['delivery'], context['total'] * settings.STANDARD_DELIVERY_PERCENTAGE / 200)

        self.assertEqual(context['total'], Decimal(str(self.product.price)))
        self.assertEqual(context['grand_total'], context['total'] + context['delivery'])

    def test_product_count(self):
        # Test the product count before adding an item
        context = cart_contents(self.client)
        self.assertEqual(context['product_count'], 0)

        # Add a test product to the cart
        self.add_sample_product_to_cart()

        # Test the product count after adding an item
        context = cart_contents(self.client)
        self.assertEqual(context['product_count'], 1)

