from django.urls import path
from . import views
app_name = 'cart'
urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('edit/<int:product_id>/', views.cart_edit, name='cart_edit'),
    path('remove/<int:product_id>/', views.cart_remove, 
                                     name='cart_remove'),
]