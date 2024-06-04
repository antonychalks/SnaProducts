from django import forms

from .models import SavedProductsList


class ListManagementForm(forms.ModelForm):
    class Meta:
        model = SavedProductsList
        exclude = ['user', 'price_total', 'item_on_sale']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
