from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client
from .models import Product, Category


# Create your tests here.
class TestProductViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_products_url = reverse('products')
        self.manage_products_url = reverse('manage_products')
        self.user = User.objects.create_superuser(
            username="testUsername",
            password="myPassword",
            email="test@test.com"
        )
        self.category1 = Category.objects.create(name='Category1', type=1)
        self.category2 = Category.objects.create(name='Category2', type=1)
        self.product1 = Product(id="98", category=self.category1, sku="TEST9999", name="test product 1",
                               description="test description", price="99.99", rating="3")
        self.product2 = Product(id="99", category=self.category2, sku="TEST9999", name="test product 2",
                               description="test description", price="39.99", rating="3")
        self.category1.save()
        self.category2.save()
        self.product1.save()
        self.product2.save()
        
    def test_render_list_products_page(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)

    def test_list_product_GET_with_search(self):
        response = self.client.get(self.list_products_url, {'search': 'test product 1'})

        self.assertTrue(any(product.name == 'test product 1' for product in response.context['products']))

    def test_list_products_GET(self):
        response = self.client.get(self.list_products_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/list_products.html')

    def test_list_products_GET_sorted_by_name_ascending(self):
        response = self.client.get(self.list_products_url, {'sort': 'name', 'direction': 'asc'})

        # Checking if the first product in the sorted context is the one with the smallest name
        self.assertEqual(response.context['products'][0], self.product1)

    def test_list_products_GET_sorted_by_name_descending(self):
        response = self.client.get(self.list_products_url, {'sort': 'name', 'direction': 'desc'})

        # Checking if the first product in the sorted context is the one with the largest name
        self.assertEqual(response.context['products'][0], self.product2)

    def test_list_products_GET_sorted_by_category(self):
        response = self.client.get(self.list_products_url, {'sort': 'category'})

        # Checking if the first product in the sorted context is the one with the category with the smallest name
        self.assertEqual(response.context['products'][0], self.product1)

    def test_list_products_GET_sorted_by_price(self):
        response = self.client.get(self.list_products_url, {'sort': 'price', 'direction': 'asc'})

        # Checking if the first product in the sorted context is the one with the category with the smallest name
        self.assertEqual(response.context['products'][0], self.product2)

    def test_render_product_details_page(self):
        response = self.client.get(reverse(
            'product_detail', args=['99']))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"test product", response.content)
        self.assertIn(b"test description", response.content)
        self.assertIn(b"9.99", response.content)
        self.assertIn(b"3", response.content)

    def test_manage_product_GET_with_search(self):
        response = self.client.get(self.manage_products_url, {'manage_search': 'test product 1'})

        self.assertTrue(any(product.name == 'test product 1' for product in response.context['products']))

    def test_manage_products_GET(self):
        response = self.client.get(self.manage_products_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/manage_products.html')

    def test_manage_products_GET_sorted_by_name_ascending(self):
        response = self.client.get(self.manage_products_url, {'sort': 'name', 'direction': 'asc'})

        # Checking if the first product in the sorted context is the one with the smallest name
        self.assertEqual(response.context['products'][0], self.product1)

    def test_manage_products_GET_sorted_by_name_descending(self):
        response = self.client.get(self.manage_products_url, {'sort': 'name', 'direction': 'desc'})

        # Checking if the first product in the sorted context is the one with the largest name
        self.assertEqual(response.context['products'][0], self.product2)

    def test_manage_products_GET_sorted_by_category(self):
        response = self.client.get(self.manage_products_url, {'sort': 'category'})

        # Checking if the first product in the sorted context is the one with the category with the smallest name
        self.assertEqual(response.context['products'][0], self.product1)

    def test_manage_products_GET_sorted_by_price(self):
        response = self.client.get(self.manage_products_url, {'sort': 'price', 'direction': 'asc'})

        # Checking if the first product in the sorted context is the one with the category with the smallest name
        self.assertEqual(response.context['products'][0], self.product2)
