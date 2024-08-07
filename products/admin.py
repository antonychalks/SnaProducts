from django.contrib import admin
from django import forms
from .models import Product, Category, Review


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the category field to display display_name instead of name
        self.fields['category'].queryset = Category.objects.filter(type=1)
        self.fields['category'].widget.choices = [(category.pk, category.display_name)
                                                  for category in self.fields['category'].queryset]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Lists fields for display in admin, fields for search,
    field filters, fields to prepopulate and rich-text editor.
    """
    form = ProductAdminForm

    list_display = ('name', 'category', 'price', 'sku',)
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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Lists fields for display in admin, fields for search,
    field filters, fields to prepopulate and rich-text editor.
    """
    list_display = ('product', 'rating', 'review', 'verified',)
    search_fields = ['product', 'rating', ]
    list_filter = ('verified',)
