from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from profiles.models import UserProfile
from .models import Product, Category, Review, Stock
from saved_products.models import SavedProductsList
from .forms import ProductManagementForm, CategoryManagementForm, ProductReviewForm, StockManagementForm


# Create your views here.
# noinspection DuplicatedCode
def list_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    display_sorting = {}
    display_category = None
    if request.user.is_authenticated:
        user = request.user.userprofile.id
        lists = SavedProductsList.objects.filter(user=user)
    else:
        lists = None

    if request.GET:
        if 'sort' in request.GET:  # Checks for sort in the request.GET so that this code gets run
            sortkey = request.GET['sort']  # Stores the request in a variable
            sort = sortkey  # Stores the sortkey variable in a variable so that the original is kept
            if sortkey == 'name':
                sortkey = 'lower_name'  # Renames sortkey to lower_name
                products = products.annotate(
                    lower_name=Lower('name'))  # Creates a temporary field on the model for lower name
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:  # Checks for a direction in the GET request
                direction = request.GET['direction']  # Stores the direction request in a variable
                # If the variable is desc for descending, it will add a minus to the front of the sortkey variable
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            else:
                direction = 'asc'
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

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            # 'i' before contains makes the query case insensitive.
            #  '|' creates or statement i.e: name = query or description = query.
            products = products.filter(queries)

        print(categories)

    sort_option = {
        'sort': sort,
        'direction': direction,
        'combined': f'{sort}_{direction}',
    }

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': sort_option,
        'display_sorting': display_sorting,
        'display_category': display_category,
        'lists': lists
    }

    return render(request, 'products/list_products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    products = get_object_or_404(Product, pk=product_id)
    lists = SavedProductsList.objects.all()
    reviews = Review.objects.filter(product=products)
    review_form = ProductReviewForm

    context = {
        'product': products,
        'lists': lists,
        'reviews': reviews,
        'form': review_form,
    }
    return render(request, 'products/product_detail.html', context)


# noinspection DuplicatedCode
@login_required
def manage_products(request):
    """ A view to manage all products, including sorting and search queries """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only shop admins can do that.')
        return redirect(reverse('home'))

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    display_sorting = {}
    display_category = None

    if request.GET:
        if 'sort' in request.GET:  # Checks for sort in the request.GET so that this code gets run
            sortkey = request.GET['sort']  # Stores the request in a variable
            sort = sortkey  # Stores the sortkey variable in a variable so that the original is kept
            if sortkey == 'name':
                sortkey = 'lower_name'  # Renames sortkey to lower_name
                products = products.annotate(
                    lower_name=Lower('name'))  # Creates a temporary field on the model for lower name
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:  # Checks for a direction in the GET request
                direction = request.GET['direction']  # Stores the direction request in a variable
                # If the variable is desc for descending it will add a minus to the front of the sortkey variable
                if direction == 'desc':
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

        if 'manage_search' in request.GET:
            query = request.GET['manage_search']
            if not query:
                messages.error(request, "You need to enter the product you are searching for.")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            # 'i' before contains makes the query case insensitive.
            #  '|' creates or statement i.e: name = query or description = query.
            products = products.filter(queries)

    sort_option = f'{sort}_{direction}'
    all_categories = Category.objects.all()

    context = {
        'all_categories': all_categories,
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': sort_option,
        'display_sorting': display_sorting,
        'display_category': display_category,
    }

    return render(request, 'products/manage_products.html', context)


def stock(request):
    """ A view to show a list of stock for all products"""
    query = None
    stock = Stock.objects.all()

    if request.GET:
        if 'manage_search' in request.GET:
            query = request.GET['manage_search']
            if not query:
                messages.error(request, "You need to enter the product you are searching for.")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            stock = stock.filter(queries)

    template = 'products/stock.html'
    context = {
        'stock': stock,
        'search_term': query,
    }

    return render(request, template, context)

# noinspection PyUnusedLocal
@login_required
def add_product(request):
    """ A view for superusers to add a new product """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only shop admins can do that.')
        return redirect(reverse('products'))

    if request.method == 'POST':
        if "cancel" in request.POST:
            product_form = ProductManagementForm()
            return redirect(reverse('add_product'))
        else:
            product_form = ProductManagementForm(request.POST, request.FILES)
            if product_form.is_valid():
                product_form.save()
                messages.success(request, 'Product added successfully')
                if "view" in request.POST:
                    return redirect(reverse('product_detail', args=[product_form.instance.id]))
                elif "manage" in request.POST:
                    product_form = ProductManagementForm()
                    return redirect(reverse('manage_products'))
                elif "return" in request.POST:
                    product_form = ProductManagementForm()
                    return redirect(reverse('add_product'))
            else:
                messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        product_form = ProductManagementForm()

    category_form = CategoryManagementForm()
    template = 'products/add.html'
    context = {
        'product_form': product_form,
        'category_form': category_form,
    }

    return render(request, template, context)


@login_required
def add_category(request):
    """ A view for superusers to add a new product """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only shop admins can do that.')
        return redirect(reverse('home'))

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
                form = CategoryManagementForm()
                messages.success(request, 'Category added successfully')
                if "manage" in request.POST:
                    return redirect(reverse('manage_products'))
                elif "return" in request.POST:
                    return redirect(reverse('add_product'))
            else:
                messages.error(request, 'Failed to add category. Please ensure the form is valid.')
    else:
        form = CategoryManagementForm()

    template = 'products/add.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_review(request, product_id):
    """ A view for users to add a new review to a product """
    product = get_object_or_404(Product, pk=product_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = ProductReviewForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            review_instance = form.save(commit=False)
            review_instance.product = product
            review_instance.author = user
            review_instance.verified = False
            for order in user_profile.orders.all():
                for lineitem in order.lineitems.all():
                    if lineitem.product == product:
                        review_instance.verified = True
                        break
            review_instance.save()
            form = CategoryManagementForm()
            messages.success(request, 'Review added successfully')
            return redirect(reverse('product_detail', args=[product_id]))
        else:
            messages.error(request, 'Failed to add review. Please ensure the form is valid.')
    else:
        form = ProductReviewForm()

    context = {
        'form': form,
    }

    template = 'products/product_detail.html'

    return render(request, template, context)


@login_required
def add_stock(request):
    """ A view for superusers to add stock for a product """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only shop admins can do that.')
        return redirect(reverse('products'))

    if request.method == 'POST':
        if "cancel" in request.POST:
            stock_form = StockManagementForm()
            return redirect(reverse('stock'))
        else:
            stock_form = StockManagementForm(request.POST, request.FILES)
            if stock_form.is_valid():
                stock_form.save()
                messages.success(request, 'Product added successfully')
                if "manage" in request.POST:
                    product_form = ProductManagementForm()
                    return redirect(reverse('stock'))
                elif "return" in request.POST:
                    product_form = ProductManagementForm()
                    return redirect(reverse('add_stock'))
            else:
                messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        stock_form = StockManagementForm()

    template = 'products/add_stock.html'
    context = {
        'stock_form': stock_form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ A view for superusers to add a new product """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only shop admins can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        if "cancel" in request.POST:
            product_form = ProductManagementForm()
            return redirect(reverse('manage_products'))
        else:
            product_form = ProductManagementForm(request.POST, request.FILES, instance=product)
            if product_form.is_valid():
                product_form.save()
                product_form = ProductManagementForm()
                messages.success(request, 'Product updated successfully')
                if "view" in request.POST:
                    return redirect(reverse('product_detail',
                                            args=[product_id]))
                elif "manage" in request.POST:
                    return redirect(reverse('manage_products'))
            else:
                messages.error(request, 'Failed to edit product. '
                                        'Please ensure the form is valid.')
    else:
        product_form = ProductManagementForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': product_form,
        'product': product,
    }

    return render(request, template, context)


# noinspection PyUnusedLocal
@login_required
def edit_category(request, category_id):
    """ A view for superusers to add a new product """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only shop admins can do that.')
        return redirect(reverse('home'))

    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        if "cancel" in request.POST:
            form = CategoryManagementForm()
            return redirect(reverse('manage_products'))
        else:
            form = CategoryManagementForm(request.POST, request.FILES, instance=category)
            if form.is_valid():
                if "parent" in request.POST == "":
                    form.save(commit=False)
                    form.instance.type = 0
                    form.save()
                else:
                    form.save()
                form = CategoryManagementForm()
                messages.success(request, 'Category added successfully')
                return redirect(reverse('manage_products'))

            else:
                messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = CategoryManagementForm(instance=category)
        messages.info(request, f'You are editing {category.get_display_name()}')

    products = Product.objects.filter(category=category_id)

    template = 'products/edit_category.html'
    context = {
        'form': form,
        'category': category,
        'products': products
    }

    return render(request, template, context)


@login_required
def edit_review(request, review_id):
    """ A view for users to edit a review """

    review = get_object_or_404(Review, pk=review_id)
    product = review.product
    if request.method == 'POST':
        if review.author == request.user:
            form = ProductReviewForm(request.POST, request.FILES, instance=review)
            if form.is_valid():
                form.save()
                form = ProductReviewForm()
                messages.success(request, 'Review updated successfully')
                return redirect(reverse('product_detail',
                                        args=[product.id]))
            else:
                messages.error(request, 'Failed to edit product. '
                                        'Please ensure the form is valid.')
        else:
            messages.error(request, 'You are not the author of this review.')
    else:  # Handle GET request here
        return redirect(reverse('products'))


@login_required
def edit_stock(request, stock_id):
    """ A view for superusers to add a new product """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only shop admins can do that.')
        return redirect(reverse('home'))

    stock = get_object_or_404(Stock, pk=stock_id)
    if request.method == 'POST':
        if "cancel" in request.POST:
            stock_form = StockManagementForm()
            return redirect(reverse('stock'))
        else:
            stock_form = StockManagementForm(request.POST, request.FILES, instance=stock)
            if stock_form.is_valid():
                stock_form.save()
                stock_form = StockManagementForm()
                messages.success(request, 'Product updated successfully')
                if "manage" in request.POST:
                    return redirect(reverse('stock'))
            else:
                messages.error(request, 'Failed to edit product. '
                                        'Please ensure the form is valid.')
    else:
        stock_form = StockManagementForm(instance=stock)
        messages.info(request, f'You are editing {stock.product.name}')

    template = 'products/edit_stock.html'
    context = {
        'form': stock_form,
        'stock': stock,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only shop admins can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('manage_products'))


@login_required
def delete_category(request, category_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only shop admins can do that.')
        return redirect(reverse('home'))

    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    messages.success(request, 'Category deleted!')
    return redirect(reverse('manage_products'))


@login_required
def delete_review(request, review_id):
    """ Delete a review"""
    review = get_object_or_404(Review, pk=review_id)
    product = review.product
    if review.author == request.user:
        review.delete()
        messages.success(request, 'Review deleted!')
    else:
        messages.error(request, 'You are not the author of this review.')
    return redirect(reverse('product_detail',
                            args=[product.id]))


@login_required
def delete_stock(request, stock_id):
    """ Delete stock from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only shop admins can do that.')
        return redirect(reverse('home'))

    stock = get_object_or_404(Stock, pk=stock_id)
    stock.delete()
    messages.success(request, 'Stock deleted!')
    return redirect(reverse('stock'))
