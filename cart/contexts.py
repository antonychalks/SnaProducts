from decimal import Decimal
from django.conf import settings

def cart_contents(request):
    cart_products = []
    total = 0
    product_count = 0
    
    if total < settings.MIN_FREE_DELIVERY:
        if total < settings.MIN_HALF_DELIVERY:
            delivery = total * Decimal((settings.STANDARD_DELIVERY_PERCENTAGE/100))
            free_delivery_delta = settings.MIN_FREE_DELIVERY - total
            half_delivery_delta = settings.MIN_HALF_DELIVERY - total
        else:
            delivery = (total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE/100)/2)
            free_delivery_delta = settings.MIN_FREE_DELIVERY - total
    else:
        delivery = 0
        free_delivery_delta = 0
        
    grand_total = delivery + total
    
    context = {
        'cart_items': cart_products,
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