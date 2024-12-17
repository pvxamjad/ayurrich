from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home , name="home"),
    path('product/<str:name>/', views.product_dtails, name="product_dtails"),
    path('shop/', views.shop, name="shop"),
    path('save-contact/', views.save_contact, name='save_contact'),
]
