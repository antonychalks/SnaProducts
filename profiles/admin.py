from django.contrib import admin

from .models import UserProfile
from saved_products.models import SavedProductsList


class SavedProductsListInline(admin.StackedInline):
    model = SavedProductsList
    can_delete = False
    verbose_name_plural = 'saved_items_list'
    extra = 0


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    inlines = (SavedProductsListInline,)

    readonly_fields = ('user', )

    fields = ('user', 'default_phone_number', 'default_first_line_address', 'default_second_line_address',
              'default_town_or_city', 'default_county', 'default_postcode', 'default_country')

    list_display = ('user',)


admin.site.register(UserProfile, UserProfileAdmin)
