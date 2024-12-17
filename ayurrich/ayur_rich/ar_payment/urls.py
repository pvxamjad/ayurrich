from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    
    path('', views.billing , name="billing"),
    path('payment-success/',views.payment_success,name="payment-success"),
    # path('payment_fail/',views.payment_fail,name="payment_fail"),
    path('save-order-summary/', views.save_order_summary, name='save_order_summary'),
    
]
