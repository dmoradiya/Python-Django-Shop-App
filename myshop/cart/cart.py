from decimal import Decimal
from unicodedata import decimal
from django.conf import settings
from shop.models import Product

class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get('cart_obj')
        if not cart:
            # save an empty cart in the session
            cart = self.session['cart_obj'] = {}
        self.cart = cart

        print('cart_obj :', cart)
      

    def add(self, product, quantity=1, addQty=False, removeQty=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price),
                                    #  'productTotalPrice': str(product.price)
                                      }

       

        if addQty:
            self.cart[product_id]['quantity'] += quantity     
            # newQty = self.cart[product_id]['quantity']       
            # self.cart[product_id]['productTotalPrice'] = str(Decimal(product.price)*newQty)
        self.save()
        
        
        if removeQty:
            # if quantity >= 1:
            #     self.cart[product_id]['quantity'] -= quantity
            
            if self.cart[product_id]['quantity'] > 1:
                self.cart[product_id]['quantity'] -= quantity
                # newQty = self.cart[product_id]['quantity']       
                # self.cart[product_id]['productTotalPrice'] = str(Decimal(product.price)*newQty)
            else:
                self.remove(product)
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            #item['price'] = Decimal(item['price'])
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item
        
    def get_product_count(self):
        """
        Count all items in the cart.
        """
        return len([key for key in self.cart.keys()])

    # Subtotal
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        
    # Total Tax
    def get_total_tax(self):
        tax = 0.05
        return round(float(self.get_total_price())*tax,2)
        
    # Total after tax
    def get_total(self):        
        return round(float(self.get_total_price())+self.get_total_tax(),2)

    def clear(self):
        # remove cart from session
        del self.session['cart_obj']
        self.save()
    