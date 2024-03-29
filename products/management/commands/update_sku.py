from django.core.management.base import BaseCommand
from products.models import Category, generate_sku

class Command(BaseCommand):
    help = 'Update product sku based on generate sku function in models.py'

    def handle(self, *args, **kwargs):
        Products = Products.objects.all()
        for product in Products:
            product.save()
        self.stdout.write(self.style.SUCCESS('Products updated successfully'))
