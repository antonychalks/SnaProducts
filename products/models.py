from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from django.contrib.auth.models import User
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone

CATEGORY_TYPE = ((0, "Parent"), (1, "Child"))
DEALS = ((0, 0), (1, 5), (2, 10), (3, 20), (4, 25))
SIZES = ((0, 'N/A'), (1, 'XS'), (2, 'S'), (3, 'M'), (4, 'L'), (5, 'XL'))


# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)
    type = models.IntegerField(choices=CATEGORY_TYPE, editable=False)
    
    def __str__(self):
        return self.name
        
    def get_display_name(self):
        return self.display_name

    def get_type(self):
        return self.get_type_display()
    
    def save(self, *args, **kwargs):
        if self.parent:
            self.type = 1  # Set type to 1 if category has a parent
        else:
            self.type = 0  # Set type to 0 if category doesn't have a parent
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey('Category', limit_choices_to={'type': 1},  null=True, blank=True,
                                 on_delete=models.SET_NULL, default=18)
    sku = models.CharField(max_length=254, unique=True, editable=False)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = CloudinaryField('image', default='placeholder')
    has_sizes = models.BooleanField(null=True, blank=True, default=False)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.sku = self.generate_sku()
        super().save(*args, **kwargs)
    
    def parent(self):
        if self.category:
            return self.category.parent
    
    def get_category_name(self):
        if self.category is not None:
            return self.category.display_name
        else:
            return "No Category"

    def delivery(self):
        percentage = Decimal(settings.STANDARD_DELIVERY_PERCENTAGE) / Decimal(100)
        delivery_cost = self.price * percentage
        rounded_delivery_cost = delivery_cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if rounded_delivery_cost > settings.MIN_HALF_DELIVERY:
            return rounded_delivery_cost/2
        elif rounded_delivery_cost > settings.MIN_FREE_DELIVERY:
            return 0
        else:
            return rounded_delivery_cost

    # noinspection PyUnusedLocal
    def generate_sku(self):
        """Generate a unique SKU"""
        category = self.category
        sku_prefix = ""
        sku_middle = ""
        sku_suffix = ""

        # Extracting first two letters of the main category name
        if self.category:
            if category.parent:
                sku_prefix = category.parent.name[:2].upper()
            else:
                sku_prefix = "NU"
        else:
            sku_prefix = "NU"

        # Creating middle two digits from the category id
        if self.category:
            sku_middle = category.name[:2].upper()
        else:
            sku_middle = "LL"

        # Creating last four digits based on the count of products in the category
        product_count = Product.objects.filter(category=category).count() + 1
        sku_suffix = str(product_count).zfill(4)

        # Check if the generated SKU already exists, if so, adjust the count
        while Product.objects.filter(sku=sku_prefix + sku_middle + sku_suffix).exists():
            product_count += 1
            sku_suffix = str(product_count).zfill(4)

        return sku_prefix + sku_middle + sku_suffix

    def average_rating(self):
        """
        Calculate and return the average rating of related Reviews.

        If no reviews exist, this method returns None.
        """
        reviews = self.Reviews.all()
        if reviews.exists():
            return round(reviews.aggregate(Avg('rating'))['rating__avg'], 2)
        else:
            return None

    @receiver([post_save, post_delete], sender='products.Review')
    def update_product_rating(sender, instance, **kwargs):
        product = instance.product
        reviews = product.Reviews.all()
        if reviews.exists():
            product.rating = round(reviews.aggregate(Avg('rating'))['rating__avg'], 2)
        else:
            product.rating = None
        product.save()


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="Reviews", blank=True, null=True)
    title = models.CharField(max_length=50, default="Review")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="Reviews", default=0)
    rating = models.IntegerField(default=1, validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    review = models.TextField(blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="Stock", blank=True, null=True)
    size = models.IntegerField(default=0, choices=SIZES)
    deal = models.IntegerField(default=0, choices=DEALS)
    date_created = models.DateTimeField(auto_now_add=True)
    quantity_available = models.IntegerField(default=0)
    quantity_requested = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name
