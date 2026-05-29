from django import forms

from crm.models import Deal, DealItem

from .base import StyledFormMixin


class DealForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Deal
        fields = ["title", "client", "stage", "owner", "source", "priority", "amount", "probability", "expected_close_date", "description"]
        widgets = {
            "expected_close_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class DealItemForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = DealItem
        fields = ["product", "name", "quantity", "price", "discount"]
