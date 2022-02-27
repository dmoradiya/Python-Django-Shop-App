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