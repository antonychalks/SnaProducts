from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from checkout.models import Order
from .forms import UserProfileForm


# Create your views here.
@login_required
def profile_view(request):
    """ A view that renders the profile page """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Profile update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all()

    saved_items_list = profile.saved_items_list.all()

    context = {
        'form': form,
        'orders': orders,
        'profile': profile,
        'on_profile_page': True,
        'saved_items_list': saved_items_list
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'Order number: {order_number} is an existing order. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'

    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)

