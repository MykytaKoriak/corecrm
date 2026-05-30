from django import forms

from crm.models import Product

from .base import StyledFormMixin


class ProductForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "sku", "category", "description", "image", "price", "cost", "stock", "status"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].widget.attrs["list"] = "product-categories"
