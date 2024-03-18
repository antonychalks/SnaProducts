from django.shortcuts import render

# Create your views here.
def index(request):
    """ A view to return the index page """

    return render(request, 'landing_page/index.html')