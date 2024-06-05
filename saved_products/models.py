from profiles.models import UserProfile
from django.db import models

from products.models import Product


# Create your models here.
class SavedProductsList(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='saved_items_list')
    name = models.CharField(max_length=100)
    description = models.TextField()
    visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    price_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    item_on_sale = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the SavedProductsItem total
        and update the order total.
        """
        super().save(*args, **kwargs)
        self.price_total = 0
        for product in self.list_product.all():
            self.price_total += product.saved_products_item_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SavedProductsItem(models.Model):
    list = models.ForeignKey(SavedProductsList, null=False, blank=False, on_delete=models.CASCADE,
                             related_name='list_product')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True)  # XS, S, M, L, XL
    saved_products_item_price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False,
                                                    editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the saved_products_item_total
        and update the list total.
        """
        self.saved_products_item_price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product.name
