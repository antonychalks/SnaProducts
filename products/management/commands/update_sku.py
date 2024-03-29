from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Update product SKU based on generate_sku function in models.py'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        for product in products:
            product.sku = product.generate_sku()
            product.save()
        self.stdout.write(self.style.SUCCESS('Products updated successfully'))
