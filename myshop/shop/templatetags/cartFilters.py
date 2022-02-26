from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()
    for productId in keys:
        if int(productId) == product.id:
            return True
    return False

@register.filter(name='cart_qty')
def cart_qty(product, cart):
    keys = cart.keys()
    for productId in keys:
        if int(productId) == product.id:
            return int(cart[productId]['quantity'])
    return 0


