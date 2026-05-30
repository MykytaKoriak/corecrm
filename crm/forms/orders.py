from django import forms
from decimal import Decimal

from crm.models import Order, OrderFile, OrderItem

from .base import StyledFormMixin


class OrderForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Order
        fields = ["client", "deal", "owner", "payment_status", "delivery_status", "work_status", "discount", "comments"]
        widgets = {"comments": forms.Textarea(attrs={"rows": 4})}


class OrderItemForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["product", "name", "quantity", "price", "discount"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = False
        self.fields["price"].required = False
        self.fields["name"].help_text = "Можно оставить пустым: название подтянется из товара."
        self.fields["price"].help_text = "Можно оставить пустым: цена подтянется из карточки товара."

    def clean_price(self):
        return self.cleaned_data.get("price") or Decimal("0.00")


class OrderFileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = OrderFile
        fields = ["title", "file", "comment"]
