from django.test import TestCase

from .forms import CategoryManagementForm, ProductManagementForm
from .models import Category


# Create your tests here.
class TestProductManagementForm(TestCase):
    def setUp(self):
        # Set up some test data
        self.misc_category = Category.objects.create(name="test", type=0, display_name="Test")
        self.regular_category = Category.objects.create(name="regular", type=0)
        self.children_category = Category.objects.create(name="child", type=1, parent=self.regular_category)

    def test_form_initialization(self):
        form = ProductManagementForm()
        expected_choices = [
            (self.misc_category.id, self.misc_category.get_display_name() + " (Default)"),
            (self.children_category.id, self.children_category.get_display_name())
        ]
        self.assertEqual(form.fields['category'].choices, expected_choices)
        for field_name, field in form.fields.items():
            assert 'border-black rounded-0' in field.widget.attrs['class']

    def test_required_fields(self):
        form = ProductManagementForm()
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['This field is required.'],
            'description': ['This field is required.'],
            'price': ['This field is required.'],
        })


    def test_product_management_form_valid_with_all_required_fields(self):
        form = ProductManagementForm({
            'category': self.misc_category.id,
            'name': 'Test_product',
            'description': 'Test_product Description',
            'price': 99.99,

        })
        self.assertTrue(form.is_valid())
