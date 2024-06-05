from django.test import TestCase

from .forms import OrderForm


# Create your tests here.
class TestOrderForm(TestCase):
    def test_form_initialization(self):
        form = OrderForm()
        self.assertTrue(form.fields['first_name'].widget.attrs['autofocus'])
        for field in form.fields:
            if field != 'country':
                self.assertTrue('stripe-style-input' in form.fields[field].widget.attrs['class'])
                self.assertFalse(form.fields[field].label)

    def test_required_fields(self):
        form = OrderForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'first_name': ['This field is required.'],
            'last_name': ['This field is required.'],
            'email': ['This field is required.'],
            'phone_number': ['This field is required.'],
            'first_line_address': ['This field is required.'],
            'town_or_city': ['This field is required.'],
            'country': ['This field is required.'],
            'postcode': ['This field is required.'],
        })

    def test_email_validation(self):
        form = OrderForm({
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'not a valid email',
            'phone_number': '1234567890',
            'first_line_address': '123 Test St',
            'town_or_city': 'Test city',
            'country': 'DK',
            'postcode': '12345',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'email': ['Enter a valid email address.']
        })

    def test_order_form_valid_with_all_required_fields(self):
        form = OrderForm({
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'testuser@example.com',
            'phone_number': '+123456789',
            'first_line_address': '123 Test St',
            'town_or_city': 'Test city',
            'country': 'DK',
            'postcode': '12345',
        })
        self.assertTrue(form.is_valid())
