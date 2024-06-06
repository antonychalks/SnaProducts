from django.contrib.auth.models import User
from django.test import TestCase, Client

from profiles.models import UserProfile
from saved_products.forms import ListManagementForm
from saved_products.models import SavedProductsList


class TestListManagementForm(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="TestUser",
                                             email="<EMAIL>",
                                             password="<PASSWORD>")
        self.user.save()

    def test_form_is_valid(self):
        """ Test the form is valid """
        self.client.login(username='TestUser', password='<PASSWORD>')
        form = ListManagementForm({
            'name': 'Test List Name',
            'description': 'Test description for the list.',
            'visible': True,
        })
        self.assertTrue(form.is_valid())


    def test_form_is_invalid(self):
        """ Test the form is invalid by not giving data for a required field"""
        self.client.login(username='TestUser', password='<PASSWORD>')
        form = ListManagementForm({
            'name': '',  # name is required, so the form should be invalid.
            'description': 'Test description for the list.',
            'visible': True,
        })
        self.assertFalse(form.is_valid())

    def test_form_saves(self):
        """ Test the form saves by checking for the list in the database. """
        self.client.login(username='TestUser', password='<PASSWORD>')
        form = ListManagementForm({
            'name': 'Test List Name',
            'description': 'Test description for the list.',
            'visible': True,
        })

        if form.is_valid():
            saved_list = form.save(commit=False)
            saved_list.user = self.user.userprofile  # Assign the UserProfile instance
            saved_list.save()

            self.assertIsInstance(saved_list, SavedProductsList)
            self.assertEqual(saved_list.name, 'Test List Name')
            self.assertEqual(saved_list.description, 'Test description for the list.')
            self.assertEqual(saved_list.visible, True)

