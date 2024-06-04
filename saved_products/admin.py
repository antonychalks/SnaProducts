from django.contrib import admin
from .models import SavedProductsList, SavedProductsItem


class SavedProductsItemAdminInline(admin.TabularInline):
    model = SavedProductsItem
    # noinspection SpellCheckingInspection
    readonly_fields = ('saved_products_item_price',)


class SavedProductsListAdmin(admin.ModelAdmin):
    inlines = (SavedProductsItemAdminInline,)

    readonly_fields = ('created_at', 'price_total', 'item_on_sale')

    fields = ('user', 'name', 'description', 'visible',
              'created_at', 'price_total', 'item_on_sale')

    list_display = ('created_at', 'name', 'description', 'visible', 'price_total', 'item_on_sale')

    ordering = ('-created_at',)


admin.site.register(SavedProductsList, SavedProductsListAdmin)
