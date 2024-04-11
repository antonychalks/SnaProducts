from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.
def list_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    
    if request.GET:
        if 'category' in request.GET:
            # if category has parent then continue, else if category has no parent, display all categories with parent of category.
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
            
        if 'search' in request.GET:
            query = request.GET['search']
            if not query:
                messages.error(request, "You need to enter the product you are searching for.")
                return redirect(reverse('products'))

            queries = Q(name__icontains = query) | Q(description__icontains = query)
            # i before contains makes the query case insensitive. | creates or statement i.e: name = query or description = query
            products = products.filter(queries)
    
    context = {
        'products': products,
        'search term': query,
        'current_categories': categories,
    }

    return render(request, 'products/list_products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    products = get_object_or_404(Product, pk=product_id)
    
    context = {
        'product': products,
    }
    return render(request, 'products/product_detail.html', context)