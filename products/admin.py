from django.contrib import admin
from django import forms
from .models import Product, Category


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the category field to display display_name instead of name
        self.fields['category'].queryset = Category.objects.filter(type=1).values_list('display_name', flat=True)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Lists fields for display in admin, fields for search,
    field filters, fields to prepopulate and rich-text editor.
    """
    form = ProductAdminForm

    list_display = ('name', 'category', 'price',)
    search_fields = ['name', 'category__display_name', ]  # Searching based on display_name
    list_filter = ('category', 'price', )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Lists fields for display in admin, fields for search,
    field filters, fields to prepopulate and rich-text editor.
    """

    list_display = ('parent', 'name', 'display_name', 'type',)
    search_fields = ['name', 'display_name', ]
    list_filter = ('parent', 'type', )
