from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.http import HttpResponseBadRequest
from products.models import Product

# Create your views here.
def view_cart(request):
    """ A view to return the contents of the cart """

    return render(request, 'cart/cart.html')

def add_to_cart(request, product_id):
    """ A view to add a product to the site cart. """
    if request.method == 'POST':
        print(request.POST)
        product = get_object_or_404(Product, id=product_id)
        redirect_url = request.POST.get('redirect_url')
        quantity = int(request.POST.get('quantity')) 
        cart = request.session.get('cart', {})
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        
        if not redirect_url:
            return HttpResponseBadRequest("Missing redirect_url")
        
        if not quantity or quantity <= 0:
            return HttpResponseBadRequest("Invalid quantity")
        
        if size:
            # Checks for the product_id in the cart
            if product_id in list(cart.keys()):
                #checks if the product with the same size is in the cart.
                if size in cart[product_id]['products_by_size'].keys():
                    #If it is then it will increase the amount of items in the bag by the quantity
                    cart[product_id]['products_by_size'][size] += quantity
                else:
                    #If the product with the size isn't in the cart, it will create a new entry.
                    cart[product_id]['products_by_size'][size] = quantity
            else:
                #If the product isn't already in the cart, it will be added now.
                cart[product_id] = {'products_by_size' : {size: quantity}}
        else:
            #If the product has no size, it'll be checked if it is in the cart.
            if product_id in list(cart.keys()):
                #If it is in the cart, increase the quantity
                cart[product_id] += quantity
            else:
                #if the cart already has the item_id, the quantity will increase by the selected quantity.
                cart[product_id] = quantity
                
        request.session['cart'] = cart
        print(f"Product ID: {product.id}, Quantity: {quantity}")
        return redirect(redirect_url)
    
    return HttpResponseBadRequest("Invalid request method")

def update_cart(request, product_id):
    """ A view to add a product to the site cart. """
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity')) 
        cart = request.session.get('cart', {})
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        
        if not quantity or quantity <= 0:
            return HttpResponseBadRequest("Invalid quantity")
        
        if size:
            if quantity > 0:
                cart[product_id]['products_by_size'][size] = quantity
            else:
                del cart[product_id]['products_by_size'][size]
                if not cart[product_id]['items_by_size']:
                    cart.pop(product_id)
        else:
            if quantity > 0:
                cart[product_id] = quantity
            else:
                cart.pop(product_id)
                
        request.session['cart'] = cart
        return redirect(reverse('view_cart'))
    
    return HttpResponseBadRequest("Invalid request method")

def remove_from_cart(request, product_id):
    """ A view to add a product to the site cart. """
    try:
        if request.method == 'POST':
            cart = request.session.get('cart', {})
            size = None
            if 'product_size' in request.POST:
                size = request.POST['product_size']
            
            if size:
                del cart[product_id]['products_by_size'][size]
                if not cart[product_id]['items_by_size']:
                    cart.pop(product_id)
            else:
                cart.pop(product_id)
                    
            request.session['cart'] = cart
            return HttpResponse(status=200)
        else:
            return HttpResponseBadRequest("Invalid request method")

    except Exception as e:
        return HttpResponse(status=500)
