from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.urls import reverse
from django.test import TestCase
from products.models import Product, Category


# Create your tests here.
class TestCartViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="testUsername",
            password="myPassword",
            email="test@test.com"
        )
        self.category = Category.objects.create(name="Miscellaneous")
        self.product = Product(id="9999", category=self.category, sku="TEST9999", name="test product",
                               description="test description", price="99.99", rating="3")
        self.product.save()

    def test_render_view_cart_page(self):
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_without_size(self):
        response = self.client.post(
            reverse('add_to_cart', args=[self.product.id]),
            data={
                'redirect_url': '/products/',
                'quantity': 5
            }
        )
        self.assertEqual(response.status_code, 302)  # 302 is the status code for a redirect
        self.assertRedirects(response, '/products/')

        # Check that the product was added to the cart with the correct quantity
        cart = self.client.session['cart']
        self.assertIn(str(self.product.id), cart)
        self.assertEqual(cart[str(self.product.id)], 5)

    def test_add_to_cart_with_size_first_time(self):
        response = self.client.post(
            reverse('add_to_cart', args=[self.product.id]),
            data={
                'redirect_url': '/products/',
                'quantity': 3,
                'product_size': 'M'
            }
        )
        self.assertEqual(response.status_code, 302)  # 302 is the status code for a redirect
        self.assertRedirects(response, '/products/')

        # Check that the product was added to the cart with the correct quantity and size
        cart = self.client.session['cart']
        self.assertIn(str(self.product.id), cart)
        self.assertIn('M', cart[str(self.product.id)]['products_by_size'])
        self.assertEqual(cart[str(self.product.id)]['products_by_size']['M'], 3)

    def test_add_to_cart_with_size_existing(self):
        # First, add the item to the cart
        self.client.post(
            reverse('add_to_cart', args=[self.product.id]),
            data={
                'redirect_url': '/products/',
                'quantity': 2,
                'product_size': 'L'
            }
        )

        # Then, add the same item with the same size again
        response = self.client.post(
            reverse('add_to_cart', args=[self.product.id]),
            data={
                'redirect_url': '/products/',
                'quantity': 4,
                'product_size': 'L'
            }
        )
        self.assertEqual(response.status_code, 302)  # 302 is the status code for a redirect
        self.assertRedirects(response, '/products/')

        # Check that the product was added to the cart with the correct quantity and size
        cart = self.client.session['cart']
        self.assertIn(str(self.product.id), cart)
        self.assertIn('L', cart[str(self.product.id)]['products_by_size'])
        self.assertEqual(cart[str(self.product.id)]['products_by_size']['L'], 6)  # 2 + 4

    def test_add_to_cart_with_invalid_size(self):
        response = self.client.post(
            reverse('add_to_cart', args=[self.product.id]),
            data={
                'redirect_url': '/products/',
                'quantity': 3,
                'product_size': 'INVALID_SIZE'  # assuming 'INVALID_SIZE' is not a valid size
            }
        )
        # Considering your code doesn't handle invalid sizes,
        # we should see a 302 status code for a successful redirect
        self.assertEqual(response.status_code, 302)
        # Check that the cart was updated with the invalid size anyway
        cart = self.client.session['cart']
        self.assertIn('INVALID_SIZE', cart[str(self.product.id)]['products_by_size'])

    def test_update_cart_quantity_to_zero(self):
        # Directly initialize the session cart
        session = self.client.session
        session['cart'] = {str(self.product.id): {'products_by_size': {'L': 2}}}

        # Ensure 'L' is in session['cart'][str(self.product.id)]['products_by_size']
        assert 'L' in session['cart'][str(self.product.id)]['products_by_size']

        session.save()

        post_data = {
            'quantity': 0,
            'product_size': 'L'
        }
        response = self.client.post(
            reverse('update_cart', args=[self.product.id]),
            data=post_data
        )

        # refresh session
        session = self.client.session

        self.assertNotIn(str(self.product.id), session['cart'])

    def test_update_cart_with_nonexistent_product(self):
        post_data = {
            'quantity': 5,
            'product_size': 'L'
        }
        random_product_id = 5678  # Make sure this ID doesn't exist
        response = self.client.post(
            reverse('update_cart', args=[random_product_id]),
            data=post_data
        )
        self.assertEqual(response.status_code, 404)

    def test_update_cart_with_invalid_size(self):
        self.client.post(
            reverse('add_to_cart', args=[self.product.id]),
            data={
                'redirect_url': '/products/',
                'quantity': 2,
                'product_size': 'L'  # Legitimate size
            }
        )
        response = self.client.post(
            reverse('update_cart', args=[self.product.id]),
            data={'quantity': 5, 'product_size': 'INVALID_SIZE'}  # assuming 'INVALID_SIZE' is not a valid size
        )
        self.assertEqual(response.status_code, 302)
        # Check that the cart was updated with the invalid size anyway
        cart = self.client.session['cart']
        self.assertIn('INVALID_SIZE', cart[str(self.product.id)]['products_by_size'])

    def test_remove_from_cart(self):
        self.client.post(
            reverse('add_to_cart', args=[self.product.id]),
            data={
                'redirect_url': '/products/',
                'quantity': 2,
                'product_size': 'L'
            }
        )
        self.client.post(
            reverse('remove_from_cart', args=[self.product.id]),
            data={
                'product_size': 'L'
            }
        )
        cart = self.client.session['cart']
        self.assertNotIn(str(self.product.id), cart)

    def test_remove_from_cart_invalid_size(self):
        self.client.post(
            reverse('add_to_cart', args=[self.product.id]),
            data={
                'redirect_url': '/products/',
                'quantity': 2,
                'product_size': 'INVALID_SIZE'  # assuming 'INVALID_SIZE' is not a valid size
            }
        )
        response = self.client.post(
            reverse('remove_from_cart', args=[self.product.id]),
            data={'product_size': 'INVALID_SIZE'}  # assuming 'INVALID_SIZE' is not a valid size
        )
        self.assertEqual(response.status_code, 200)
        # Check that the cart doesn't contain the product anymore
        cart = self.client.session['cart']
        self.assertNotIn(str(self.product.id), cart)

    def test_invalid_request_method(self):
        response = self.client.get(reverse('update_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 400)  # Bad Request

    def test_invalid_remove_request_method(self):
        response = self.client.get(reverse('remove_from_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 400)  # Bad Request

