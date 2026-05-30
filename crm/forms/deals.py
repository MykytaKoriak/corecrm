from django import forms
from decimal import Decimal

from crm.models import Deal, DealItem

from .base import StyledFormMixin


class DealForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Deal
        fields = ["title", "client", "stage", "owner", "source", "priority", "amount", "expected_close_date", "description"]
        widgets = {
            "expected_close_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].required = False
        self.fields["title"].help_text = "Можно оставить пустым: CRM сформирует название из клиента и первого товара."


class DealItemForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = DealItem
        fields = ["product", "name", "quantity", "price", "discount"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = False
        self.fields["price"].required = False
        self.fields["name"].help_text = "Можно оставить пустым: название подтянется из товара."
        self.fields["price"].help_text = "Можно оставить пустым: цена подтянется из карточки товара."

    def clean_price(self):
        return self.cleaned_data.get("price") or Decimal("0.00")
