from django.shortcuts import render
from .models import Product

# Create your views here.
def list_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    
    context = {
        'products': products,
    }

    return render(request, 'products/list_products.html', context)