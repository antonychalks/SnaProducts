from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required

from products.models import Product
from .forms import ListManagementForm
from .models import SavedProductsList, SavedProductsItem


def list_detail(request, list_id):
    """ A view to show individual list details and products on the list """

    saved_products_list = get_object_or_404(SavedProductsList, pk=list_id)
    saved_products_items = saved_products_list.list_product.all()

    context = {
        'list': saved_products_list,
        'items': saved_products_items,
        'on_list_page': True,
    }
    return render(request, 'saved_products/list_detail.html', context)


# Create your views here.
@login_required
def create_list(request):
    """ A view for logged-in users to create a new list of saved products. """

    if request.method == 'POST':
        if "cancel" in request.POST:
            return redirect(reverse('profile'))
        else:
            form = ListManagementForm(request.POST)
            if form.is_valid():
                sp_list = form.save(commit=False)
                sp_list.user = request.user.userprofile
                sp_list.save()
                messages.success(request, f'List {form.instance.name} created successfully')
                return redirect(reverse('list_detail', args=[form.instance.id]))
            else:
                messages.error(request, 'Failed to create list. Please ensure the form is valid.')
    else:
        list_management_form = ListManagementForm()

    template = 'saved_products/create_list.html'
    context = {
        'list_management_form': list_management_form,
    }

    return render(request, template, context)


@login_required
def delete_list(request, list_id):
    """ Delete a list from the store """
    list = get_object_or_404(SavedProductsList, pk=list_id)
    list.delete()
    messages.success(request, 'List deleted!')
    return redirect(reverse('profile'))

@login_required
def edit_list(request, list_id):
    """ A view for users to edit a list """
    list = get_object_or_404(SavedProductsList, pk=list_id)
    if request.method == 'POST':
        if "cancel" in request.POST:
            form = ListManagementForm()
            return redirect(reverse('list', args=[form.instance.id]))
        else:
            form = ListManagementForm(request.POST, instance=list)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product updated successfully')
                if "view" in request.POST:
                    return redirect(reverse('list_detail', args=[form.instance.id]))
                elif "profile" in request.POST:
                    return redirect(reverse('profile'))
            else:
                messages.error(request, 'Failed to edit product. Please ensure the form is valid.')
    else:
        form = ListManagementForm(instance=list)
        messages.info(request, f'You are editing {list.name}')

    template = 'saved_products/edit_list.html'
    context = {
        'form': form,
        'list': list,
    }

    return render(request, template, context)


def add_to_list(request, product_id):
    """ A view to add a product to a list. """

    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        redirect_url = request.POST.get('redirect_url')
        selected_list_id = request.POST.get('list_selector')
        selected_list = SavedProductsList.objects.get(id=selected_list_id)

        if not redirect_url:
            return HttpResponseBadRequest("Missing redirect_url")

        # Check if product already exists in the list
        new_item, created = SavedProductsItem.objects.get_or_create(
            list=selected_list,
            product=product
        )
        selected_list.save()

        if created:
            messages.success(request, 'Product added to list successfully')
            request.session['item_added_to_cart'] = False
        else:
            messages.info(request, 'Product already exists in the list')
            request.session['item_added_to_cart'] = False

        return redirect(redirect_url)

    return HttpResponseBadRequest("Invalid request method")


def remove_from_list(request, product_id):
    """ A view to delete a product from the saved list. """
    try:
        product = get_object_or_404(Product, pk=product_id)
        if request.method == 'POST':
            # Get the SavedProductsItem instance with the product
            saveditem = SavedProductsItem.objects.get(product=product)
            associated_list = saveditem.list
            saveditem.delete()
            associated_list.save()
            messages.success(request, f'Removed product{product.name} from your list')
            return HttpResponse(status=200)
        else:
            return HttpResponseBadRequest("Invalid request method")
    except Exception as e:
        messages.error(request, f'Failed to remove product: {product.name} from your list. Error: {e}')
        return HttpResponse(status=500)
