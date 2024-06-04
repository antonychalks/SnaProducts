from django import template


register = template.Library()  # Sends the tool to the library to be used


@register.filter(name='calc_subtotal')  # Sends the tool to the library to be used
def calc_subtotal(price, quantity):
    """ Calculates the subtotal for each product."""
    return price * quantity
