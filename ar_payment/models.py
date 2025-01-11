from django.db import models

from ar_store.models import ProductRegistration  # Import your Product model
# Create your models here.
from django.db.models import JSONField  # Use JSONField for structured data storage
import datetime
class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.TextField(max_length=500)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pincode = models.CharField(max_length=255)
    country = models.CharField(max_length=255,default="India")

    # dont pluralize address 
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f"Shipping Address - {str(self.full_name)}"
    


class OrderProducts(models.Model):
    session_id = models.CharField(max_length=255)  # Unique identifier for the session
    product = models.ForeignKey(ProductRegistration, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Session: {self.session_id}, Product: {self.product.name}, Quantity: {self.quantity}, Total: {self.total_price}"
    




class OrderSummary(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    shipping_info = models.JSONField()  # Assuming you want to store shipping info as JSON
    order_products = models.JSONField()  # Ensure this field is defined
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Ensure this field is defined
    is_shipped = models.BooleanField(default=False,null=True,blank=True)
    orderd_date = models.DateField(auto_now_add=True, blank=True, null=True)
    razorpay_id = models.CharField(max_length=100, unique=True,blank=True, null=True)
    shipped_date = models.DateTimeField(null=True, blank=True)  # Date when the order was shipped

    def __str__(self):
        return self.order_id
