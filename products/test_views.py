from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .models import Product, Category

# Create your tests here.
class TestProductViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="testUsername",
            password="myPassword",
            email="test@test.com"
        )
        self.category = Category.objects.create(name="Miscellaneous")
        self.product = Product(id="99", category=self.category, sku="TEST9999", name="test product", description="test description", price="99.99", rating="3")
        self.product.save()
        
    def test_render_list_products_page(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        
    def test_render_product_details_page(self):
        response = self.client.get(reverse(
            'product_detail', args=['99']))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"test product", response.content)
        self.assertIn(b"test description", response.content)
        self.assertIn(b"9.99", response.content)
        self.assertIn(b"3", response.content)
        