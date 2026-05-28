from django import forms

from crm.models import Order, OrderItem

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
