from django.shortcuts import render, redirect

# Create your views here.
def view_cart(request):
    """ A view to return the contents of the cart """

    return render(request, 'cart/cart.html')

def add_to_cart(request):
    """ A view to add a product to the site cart. """
    redirect_url = request.POST.get('redirect_url')
    
    return redirect(redirect_url)
    
    # quantity = int(request.POST.get('quantity'))
    # redirect_url = request.POST.get('redirect_url')
    # size = None
    # if 'product_size' in request.POST:
    #     size = request.POST['product_size']
    # bag = request.session.get('bag', {})
    # # Session is information stored when the server and client are communicating. 
    # #This line gets the bag from the session if there is one, or creates a bag instance if it doesn't.
    
    # if size:
    #     if item_id in list(bag.keys()):
    #         if size in bag[item_id]['items_by_size'].keys():
    #             bag[item_id]['items_by_size'][size] += quantity
    #         else:
    #             bag[item_id]['items_by_size'][size] = quantity
    #     else:
    #         bag[item_id] = {'items_by_size' : {size: quantity}}
    # else:
    #     if item_id in list(bag.keys()):
    #         bag[item_id] += quantity
    #     else:
    #         bag[item_id] = quantity
    #         #if the bag already has the item_id, the quantity will increase by the selected quantity, if the ID isn't in the bag, it will add it with the selected quantity.

    # request.session['bag'] = bag
    # return redirect(redirect_url)