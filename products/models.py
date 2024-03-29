from django.db import models
from cloudinary.models import CloudinaryField

CATEGORY_TYPE = ((0, "Main"), (1, "Sub"))

# Create your models here.
class Category(models.Model):
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    name  = models.CharField(max_length=254)
    display_name  = models.CharField(max_length=254, null=True, blank=True)
    type = models.IntegerField(choices=CATEGORY_TYPE, editable=False)
    
    def __str__(self):
        return self.name
    
    def get_display_name(self):
        return self.display_name
    
    def save(self, *args, **kwargs):
        if self.parent:
            self.type = 1  # Set type to 1 if category has a parent
        else:
            self.type = 0  # Set type to 0 if category doesn't have a parent
        super(Category, self).save(*args, **kwargs)
    
class Product(models.Model):
    category = models.ForeignKey('Category', limit_choices_to={'type': 1},  null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, unique=True, editable=False)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = CloudinaryField('image', default='placeholder')
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.sku = self.generate_sku()
        super().save(*args, **kwargs)
    
    def generate_sku(self):
        """Generate a unique SKU"""
        category = self.category
        sku_prefix = ""
        sku_middle = ""
        sku_suffix = ""

        # Extracting first two letters of the main category name
        sku_prefix = category.parent.name[:2].upper()

        # Creating middle two digits from the category id
        sku_middle = category.name[:2].upper()

        # Creating last four digits based on the count of products in the category
        product_count = Product.objects.filter(category=category).count() + 1
        sku_suffix = str(product_count).zfill(4)

        # Check if the generated SKU already exists, if so, adjust the count
        while Product.objects.filter(sku=sku_prefix + sku_middle + sku_suffix).exists():
            product_count += 1
            sku_suffix = str(product_count).zfill(4)

        return sku_prefix + sku_middle + sku_suffix

