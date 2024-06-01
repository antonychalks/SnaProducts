from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .forms import UserProfileForm

# Create your views here.
def profile(request):
    """ A view that renders the profile page """
    profile = get_object_or_404(UserProfile, user=request.user)
    form = UserProfileForm(instance=profile)

    context = {
        'form': form
    }
    return render(request, 'profiles/profile.html')