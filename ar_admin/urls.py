from django.contrib import admin
from django.urls import path,include
from . import views,admin_login

urlpatterns = [
    path('',admin_login.admin_login,name="admin_login"),
    path('logout/',admin_login.admin_logout,name="logout"),
    path('admin_home/',views.admin_home,name="admin_home"),
    path('all-products/',views.all_products,name="all-products"),
    path('all-products/add-product',views.add_product,name="add-product"),
    path('all-products/delete-product/<int:pk>/', views.delete_product, name='delete-product'),  # New URL for delete
    path('all-products/product-details/<int:pk>/',views.details,name="all-products/product-details"),
    path('all-orders/',views.all_orders,name="all-orders"),
    path('all-orders/order-details/<str:pk>/',views.order_details,name="all-orders/order-details"),
    path('product-shipping/',views.product_shipping,name="product-shipping"),
    path('product-shipping/mark-not-shipped/<int:order_id>/', views.mark_as_not_shipped, name='mark_as_not_shipped'),
    path('product-shipping/mark_as_shipped/<int:order_id>/', views.mark_as_shipped, name='mark_as_shipped'),
    path('completed-orders/',views.completed_orders,name="completed-orders"),
    path('all-contacts/',views.all_contacts,name="all-contacts"),
]
