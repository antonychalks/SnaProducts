from django.contrib.auth.models import User
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
        self.product = Product(id="9999", category=self.category, sku="TEST9999", name="test product", description="test description", price="99.99", rating="3")
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