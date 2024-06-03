from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row
from django import forms

from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductManagementForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parent_categories = Category.objects.filter(type=0)

        image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

        choices = []
        for parent in parent_categories:
            if parent.name == "misc":
                display_name = parent.get_display_name() + " (Default)"
                choices.insert(0, (parent.id, display_name))  # add as flat option
            else:
                # Only get children categories if parent is not 'special_offers' or 'misc'
                children_in_parent = Category.objects.filter(parent=parent)
                category_choices = [
                    (category.id, category.get_display_name()) for category in children_in_parent
                ]
                choices.append((parent.get_display_name(), category_choices))  # add as optgroup
        self.fields['category'].choices = choices

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


class CategoryManagementForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parent_categories = Category.objects.filter(type=0)
        choices = [(parent.id, parent.get_display_name()) for parent in parent_categories]
        no_parent = (None, "Category is a parent.")
        choices.insert(0, no_parent)

        self.fields['parent'].choices = choices

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
