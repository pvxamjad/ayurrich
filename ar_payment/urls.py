from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    
    path('', views.billing , name="billing"),
    path('payment-success/',views.payment_success,name="payment-success"),
    # path('payment_fail/',views.payment_fail,name="payment_fail"),
    path('save-order-summary/', views.save_order_summary, name='save_order_summary'),
    path("create-razorpay-order/", views.create_razorpay_order, name="create_razorpay_order"),
    path("verify-razorpay-payment/", views.verify_razorpay_payment, name="verify_razorpay_payment"),
]
