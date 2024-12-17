from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
    full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Fullname'}), required=True)
    email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}), required=True)
    address = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}), required=True)
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'City'}), required=True)
    state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'State'}), required=True)
    pincode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Pincode'}), required=True)
    country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Country','value':'India'}), required=False, disabled=True,initial="India")
	
    class Meta:
        model = ShippingAddress
        fields = ['full_name','email','address','city','state','pincode','country']
        exclude = ['user',]
