from django.core.management.base import BaseCommand
from products.models import Category

class Command(BaseCommand):
    help = 'Update category types based on parent relationship'

    def handle(self, *args, **kwargs):
        categories = Category.objects.all()
        for category in categories:
            category.save()
        self.stdout.write(self.style.SUCCESS('Categories updated successfully'))
