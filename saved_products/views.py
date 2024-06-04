from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ListManagementForm
from .models import SavedProductsList, SavedProductsItem


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
                form.save()
                messages.success(request, f'List {form.instance.name} created successfully')
                return redirect(reverse('view_list', args=[form.instance.id]))
            else:
                messages.error(request, 'Failed to create list. Please ensure the form is valid.')
    else:
        ListManagementForm = ListManagementForm()

    template = 'saved_products/create_list.html'
    context = {
        'list_management_form': ListManagementForm,
    }

    return render(request, template, context)
