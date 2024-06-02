from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductManagementForm, CategoryManagementForm


# Create your views here.
def list_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    display_sorting = {}
    display_category = None
    
    if request.GET:
        if 'sort' in request.GET: # Checks for sort in the request.GET so that this code gets run
            sortkey = request.GET['sort'] # Stores the request in a varaible
            sort = sortkey # Stores the sortkey variable in a variable so that the original is kept
            if sortkey == 'name':
                sortkey = 'lower_name' # Renames sortkey to lower_name
                products = products.annotate(lower_name=Lower('name'))# Creates a temporary field on the model for lower name
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET: # Checks for a direction in the GET request
                direction = request.GET['direction'] # Stores the direction request in a variable
                if direction == 'desc': # If the variable is desc for descending it will add a minus to the front of the sortkey varible
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            display_sorting = sort.capitalize()
        
        if 'category' in request.GET:
            selected_categories = request.GET['category'].split(',')
            categories = []

            for category_name in selected_categories:
                category = Category.objects.get(name=category_name)
                categories.append(category)  # Add the selected category

                if category.type == 0:
                    categories.extend(category.children.all())  # Add children categories if it's a parent category

            all_category_names = [cat.name for cat in categories]
            products = products.filter(category__name__in=all_category_names)


            display_category = str(categories[0]).replace("_", " ").title()

            
        if 'search' in request.GET:
            query = request.GET['search']
            if not query:
                messages.error(request, "You need to enter the product you are searching for.")
                return redirect(reverse('products'))

            queries = Q(name__icontains = query) | Q(description__icontains = query)
            # i before contains makes the query case insensitive. | creates or statement i.e: name = query or description = query
            products = products.filter(queries)
            
        print(categories)
    
    sort_option = f'{sort}_{direction}'
    
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': sort_option,
        'display_sorting': display_sorting,
        'display_category': display_category,
    }

    return render(request, 'products/list_products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    products = get_object_or_404(Product, pk=product_id)
    
    context = {
        'product': products,
    }
    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """ A view for syperusers to add a new product """
    if request.method == 'POST':
        if "cancel" in request.POST:
            product_form = ProductManagementForm()
            return redirect(reverse('add_product'))
        else:
            product_form = ProductManagementForm(request.POST, request.FILES)
            if product_form.is_valid():
                product_form.save()
                product_form = ProductManagementForm()
                messages.success(request, 'Product added successfully')
                if "view" in request.POST:
                    return redirect(reverse('product_detail', args=[product_form.instance.id]))
                elif "manage" in request.POST:
                    return redirect(reverse('add_product'))
                elif "return" in request.POST:
                    return redirect(reverse('add_product'))
            else:
                messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        product_form = ProductManagementForm()

    category_form = CategoryManagementForm()
    template = 'products/add_product.html'
    context = {
        'product_form': product_form,
        'category_form': category_form,
    }

    return render(request, template, context)


def add_category(request):
    """ A view for syper users to add a new product """
    if request.method == 'POST':
        if "cancel" in request.POST:
            form = CategoryManagementForm()
            return redirect(reverse('add_product'))
        else:
            form = CategoryManagementForm(request.POST, request.FILES)
            if form.is_valid():
                if "parent" in request.POST == "":
                    form.save(commit=False)
                    form.instance.type = 0
                    form.save()
                else:
                    form.save()
                form = ProductManagementForm()
                messages.success(request, 'Category added successfully')
                if "manage" in request.POST:
                    return redirect(reverse('add_product'))
                elif "return" in request.POST:
                    return redirect(reverse('add_product'))
            else:
                messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductManagementForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
