from django import forms
from decimal import Decimal

from crm.models import Deal, DealItem

from .base import StyledFormMixin


class DealForm(StyledFormMixin, forms.ModelForm):
    new_client_name = forms.CharField(label="Новый клиент", required=False, help_text="Заполните, если клиента еще нет в базе.")
    new_client_company = forms.CharField(label="Компания нового клиента", required=False)
    new_client_phone = forms.CharField(label="Телефон нового клиента", required=False)
    new_client_email = forms.EmailField(label="Email нового клиента", required=False)

    class Meta:
        model = Deal
        fields = ["title", "client", "stage", "owner", "source", "priority", "amount", "expected_close_date", "description"]
        widgets = {
            "expected_close_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["client"].required = False
        self.fields["title"].required = False
        self.fields["title"].help_text = "Можно оставить пустым: CRM сформирует название из клиента и первого товара."

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("client") and not cleaned.get("new_client_name"):
            raise forms.ValidationError("Выберите клиента или заполните поле нового клиента.")
        return cleaned


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
