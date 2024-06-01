from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_cart',
                       'stripe_pid')

    fields = ('order_number', 'date', 'first_name',
              'last_name', 'email', 'phone_number',
              'country', 'postcode', 'town_or_city',
              'first_line_address','second_line_address',
              'county', 'delivery_cost', 'order_total',
              'grand_total', 'original_cart',
              'stripe_pid', 'user_profile')

    list_display = ('order_number', 'date', 'first_name',
                    'last_name', 'order_total',
                    'delivery_cost', 'grand_total',)

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)
