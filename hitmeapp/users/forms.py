from django.forms import ModelForm
from .models import Product
from django import forms


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['user',]
        fields = ['name','price','location','category','desc','contact','image',]
        
    
