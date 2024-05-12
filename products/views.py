from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category

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
        if 'sort' in request.GET: #Checks for sort in the request.GET so that this code gets run
            sortkey = request.GET['sort'] #stores the request in a varibale
            sort = sortkey #stores the sortkey variable in a varibale so that the original is kept
            if sortkey == 'name':
                sortkey = 'lower_name' #renames sortkey to lower_name
                products = products.annotate(lower_name=Lower('name'))#creates a temporary field on the model for lower name
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET: #checks for a direction in the GET request
                direction = request.GET['direction'] #stores the direction request in a variable
                if direction == 'desc': #if the variable is desc for descending it will add a minus to the front of the sortkey varible
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            display_sorting = sort.capitalize()
        
        # if 'category' in request.GET:
        #     # if category has parent then continue, else if category has no parent, display all categories with parent of category.
        #     categories = request.GET['category'].split(',')
        #     parent_categories = Category.objects.filter(type=0)
        #     categories = Category.objects.filter(name__in=categories)
        #     for category in categories:
        #         for c in parent_categories:
        #             if category == c:
        #                 parent = Category.objects.filter(name=c)
        #                 children = parent[0].children.all()
        #                 products = products.filter(category__name__in=children)
        #                 print(categories)
        #                 print(children)
        #                 print(products)
        #             else:
        #                 products = products.filter(category__name__in=categories)
        #                 print(products)
        
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