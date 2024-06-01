from django.shortcuts import render

# Create your views here.
def profile(request):
    """ A view that renders the profile page """
    context = {

    }
    return render(request, 'profiles/profile.html')