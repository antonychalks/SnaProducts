from django.test import TestCase

from .forms import CategoryManagementForm, ProductManagementForm
from .models import Category


# Create your tests here.
class TestProductManagementForm(TestCase):
    def setUp(self):
        # Set up some test data
        self.misc_category = Category.objects.create(name="test", type=0, display_name="Test")
        self.regular_category = Category.objects.create(name="regular", type=0, display_name="Regular")
        self.children_category = Category.objects.create(name="child", type=1,
                                                         parent=self.regular_category,
                                                         display_name="child_test")

        self.misc_category.save()
        self.regular_category.save()
        self.children_category.save()

    def test_form_initialization(self):
        form = ProductManagementForm()
        expected_choices = [
            ('Test', []),
            ('Regular', [(self.children_category.id, self.children_category.get_display_name())])
        ]
        actual_choices = form.fields['category'].choices
        self.assertEqual(expected_choices, actual_choices)
        for field_name, field in form.fields.items():
            assert 'border-black rounded-0' in field.widget.attrs['class']

    def test_product_management_form_valid_with_all_required_fields(self):
        form = ProductManagementForm({
            'category': self.children_category,
            'name': 'Test_product',
            'description': 'Test_product Description',
            'price': 99.99,
            # Add other fields if they are required
        })

        # print out the form errors here
        if not form.is_valid():
            print(form.errors)

        self.assertTrue(form.is_valid())
