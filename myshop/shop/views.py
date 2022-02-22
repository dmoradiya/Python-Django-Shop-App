from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator
from django.views import View
from django.conf import settings


# List View Page
class Product_List(View):

    
        

    def get(self, request, category_slug=None):
        
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available = True)


        if category_slug:
            category = get_object_or_404(Category, slug=(category_slug))
            products = products.filter(category = category)

        paginator = Paginator(products, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        
        return render(request, 
                        'shop/product/list.html',
                        {
                            'category' : category,
                            'categories' : categories,
                            'products' : page_obj                           
                        })

    def post(self, request):

        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

        # Get ProductID from add to cart form
        productId = request.POST.get('productId')
        removeQty = request.POST.get('removeQty')

        cart = request.session.get('cart')       
        
        if cart:
            quantity = cart.get(productId)
            print('qty',quantity)
           
            if quantity:
                if removeQty:
                    if quantity <= 1:
                        cart.pop(productId)
                    else:
                        cart[productId] = quantity - 1

                else:
                    cart[productId] = quantity + 1
            else:
                cart[productId] = 1
        else:
            cart = {}
            cart[productId] = 1

        request.session['cart'] = cart

        print('cart :', request.session['cart'])
        
        return redirect('/')

# Detail View Page
def product_detail(request, id, slug):

    product = get_object_or_404(Product, 
                                id=id,
                                slug=slug,
                                available=True)

    # add_to_cart_product_form = CartAddProductForm()
    return render(request, 
                'shop/product/detail.html',
                {'product': product})