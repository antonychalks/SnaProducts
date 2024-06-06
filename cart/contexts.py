from decimal import Decimal, ROUND_DOWN
from django.shortcuts import get_object_or_404
from django.conf import settings
from products.models import Product


def cart_contents(request):
    """ Controls the data for the shopping cart."""
    cart_products = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})
    
    for product_id, product_data in cart.items():
        if isinstance(product_data, int):
            # Gets the product by the item_id
            product = get_object_or_404(Product, pk=product_id)

            # Add the value of the products price * quantity of the product, and adds it to the total.
            total += product_data * product.price

            # Adds the quantity to the product count
            product_count += product_data

            # Adds the product details to the cart_products list.
            cart_products.append({
                'product_id': product_id,
                'quantity': product_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=product_id)
            for size, quantity in product_data['products_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                cart_products.append({
                    'product_id': product_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })
    
    if total < settings.MIN_FREE_DELIVERY:
        if total < settings.MIN_HALF_DELIVERY:
            delivery = total * Decimal((settings.STANDARD_DELIVERY_PERCENTAGE/100))
            delivery = delivery.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
            free_delivery_delta = settings.MIN_FREE_DELIVERY - total
            half_delivery_delta = settings.MIN_HALF_DELIVERY - total
        else:
            delivery = (total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE/100)/2)
            delivery = delivery.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
            free_delivery_delta = settings.MIN_FREE_DELIVERY - total
            half_delivery_delta = settings.MIN_HALF_DELIVERY - total
    else:
        delivery = 0
        free_delivery_delta = 0
        half_delivery_delta = 0
        
    grand_total = delivery + total
    
    context = {
        'cart_products': cart_products,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'half_delivery_delta': half_delivery_delta,
        'min_free_delivery': settings.MIN_FREE_DELIVERY,
        'min_half_delivery': settings.MIN_HALF_DELIVERY,
        'grand_total': grand_total,
    }
    
    return context
