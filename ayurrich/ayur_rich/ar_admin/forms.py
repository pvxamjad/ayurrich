from django import forms
from ar_store.models import ProductRegistration

class ProductRegistrationForm(forms.ModelForm):
    class Meta:
        model = ProductRegistration
        fields = ['name', 'image', 'description', 'health_benefits', 'quantity', 'category', 'price', 'discount_price']