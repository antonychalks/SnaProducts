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
        self.add_product_url = reverse('add_product')
        self.user = User.objects.create_superuser(
            username="testUsername",
            password="myPassword",
            email="test@test.com"
        )
        self.userNotSuper = User.objects.create_user(
            username="testNotSuperUsername",
            password="myPassword",
            email="test2@test.com"
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

        # Checking if the clfirst product in the sorted context is the one with the largest name
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
        self.client.login(username="testUsername", password="myPassword")
        response = self.client.get(self.manage_products_url, {'manage_search': 'test product 1'})

        self.assertTrue(any(product.name == 'test product 1' for product in response.context['products']))

    def test_manage_products_GET(self):
        self.client.login(username="testUsername", password="myPassword")
        response = self.client.get(self.manage_products_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/manage_products.html')

    def test_manage_products_GET_sorted_by_name_ascending(self):
        self.client.login(username="testUsername", password="myPassword")
        response = self.client.get(self.manage_products_url, {'sort': 'name', 'direction': 'asc'})

        # Checking if the first product in the sorted context is the one with the smallest name
        self.assertEqual(response.context['products'][0], self.product1)

    def test_manage_products_GET_sorted_by_name_descending(self):
        self.client.login(username="testUsername", password="myPassword")
        response = self.client.get(self.manage_products_url, {'sort': 'name', 'direction': 'desc'})

        # Checking if the first product in the sorted context is the one with the largest name
        self.assertEqual(response.context['products'][0], self.product2)

    def test_manage_products_GET_sorted_by_category(self):
        self.client.login(username="testUsername", password="myPassword")
        response = self.client.get(self.manage_products_url, {'sort': 'category'})

        # Checking if the first product in the sorted context is the one with the category with the smallest name
        self.assertEqual(response.context['products'][0], self.product1)

    def test_manage_products_GET_sorted_by_price(self):
        self.client.login(username="testUsername", password="myPassword")
        response = self.client.get(self.manage_products_url, {'sort': 'price', 'direction': 'asc'})

        # Checking if the first product in the sorted context is the one with the category with the smallest name
        self.assertEqual(response.context['products'][0], self.product2)

    def test_redirect_if_not_logged_in_as_superuser(self):
        """ Test to confirm redirection when a non-superuser is making the request """
        self.client.login(username="testNotSuperUsername", password="myPassword")
        response = self.client.get(self.add_product_url)
        self.assertRedirects(response, reverse('products'))

    def test_logged_in_with_superuser(self):
        """ Test to confirm a superuser is allowed into the page """
        self.client.login(username="testUsername", password="myPassword")
        response = self.client.get(self.add_product_url)
        self.assertEqual(response.status_code, 200)

    def test_http_method_post_with_form_data(self):
        """ Test to confirm form post is working and the page is redirecting to correct page """
        self.client.login(username="testUsername", password="myPassword")
        data = {
            "id": 9955,
            "name": "TestProduct",
            "description": "This is a product test",
            "price": 20,
            "image": "test_image.png"
        }

        response = self.client.post(self.add_product_url, data)
        self.assertEqual(response.status_code, 200)

    def test_edit_category_GET(self):
        self.client.login(username="testUsername", password="myPassword")
        response = self.client.get(reverse('edit_category', args=[self.category1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/edit_category.html')

    def test_edit_category_POST(self):
        self.client.login(username="testUsername", password="myPassword")
        response = self.client.post(reverse('edit_category', args=[self.category1.id]), {
            'name': 'New Category Name',
            'parent': '',  # Assuming no parent
        })

        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, 'New Category Name')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('manage_products'))

    def test_delete_product_POST(self):
        self.client.login(username="testUsername", password="myPassword")
        response = self.client.post(reverse('delete_product', args=[self.product1.id]))

        self.assertFalse(Product.objects.filter(id=self.product1.id).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('manage_products'))

    def test_delete_category_POST(self):
        self.client.login(username="testUsername", password="myPassword")
        response = self.client.post(reverse('delete_category', args=[self.category1.id]))

        self.assertFalse(Category.objects.filter(id=self.category1.id).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('manage_products'))
