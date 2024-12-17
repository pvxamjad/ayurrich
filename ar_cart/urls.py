from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    
    path('', views.cart , name="cart"),
    path('add_cart', views.add_cart, name="add_cart"),
    path('update-cart-qty/', views.update_cart_qty, name='update_cart_qty'),
    path('remove-cart-item/', views.remove_cart_item, name='remove_cart_item'),
]
