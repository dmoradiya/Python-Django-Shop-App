from operator import add
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from shop.models import Product
from .cart import Cart
# from .forms import CartAddProductForm

@require_POST
def cart_edit(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # form = CartAddProductForm(request.POST)
    # if form.is_valid():
        # cd = form.cleaned_data
    # Get ProductID from add to cart form

    addQty = request.POST.get('addQty')
    removeQty = request.POST.get('removeQty')
    if addQty:
        cart.add(product=product,
                 addQty=addQty
                )

    if removeQty:
        cart.add(product=product,
                 removeQty=removeQty
                )

    
    # return redirect('shop:product_list')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    # for item in cart:
    #     item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})