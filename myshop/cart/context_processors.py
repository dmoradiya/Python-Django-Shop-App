from .cart import Cart

def cart(request):
    return {'cartContext': Cart(request)}