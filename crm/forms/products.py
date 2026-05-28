from django import forms

from crm.models import Product

from .base import StyledFormMixin


class ProductForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "sku", "category", "image", "price", "cost", "stock", "status"]
