from django.db import models

CATEGORY_TYPE = ((0, "Main"), (1, "Sub"))

# Create your models here.
class Category(models.Model):
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
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
def generate_sku(product):
    """Generate a unique SKU"""
    category = product.category
    sku_prefix = ""
    sku_middle = ""
    sku_suffix = ""

    # Extracting first two letters of the main category name
    if category.parent:
        sku_prefix = category.parent.name[:2].upper()
    else:
        sku_prefix = category.name[:2].upper()

    # Creating middle two digits from the category id
    sku_middle = category.name[:2].upper()

    # Creating last four digits based on the count of products in the category
    sku_suffix = str(Product.objects.filter(category=category).count() + 1).zfill(4)

    return sku_prefix + sku_middle + sku_suffix