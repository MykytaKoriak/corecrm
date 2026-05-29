from django import forms

from crm.models import BotLead, CallLog, DocumentTemplate, InboxMessage, Shipment

from .base import StyledFormMixin


class InboxMessageForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = InboxMessage
        fields = ["channel", "sender_name", "sender_handle", "text", "client", "deal", "status"]
        widgets = {"text": forms.Textarea(attrs={"rows": 4})}


class BotLeadForm(StyledFormMixin, forms.ModelForm):
    create_client_and_deal = forms.BooleanField(label="Создать клиента и сделку", required=False, initial=True)

    class Meta:
        model = BotLead
        fields = ["source", "name", "phone", "email", "message", "create_client_and_deal"]
        widgets = {"message": forms.Textarea(attrs={"rows": 4})}


class CallLogForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CallLog
        fields = ["direction", "status", "phone", "client", "assigned_to", "recording", "comment", "called_at"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3}),
            "called_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class ShipmentForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ["order", "provider", "tracking_number", "status", "recipient_city", "recipient_warehouse"]


class DocumentTemplateForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = DocumentTemplate
        fields = ["name", "template_type", "body", "is_active"]
        widgets = {"body": forms.Textarea(attrs={"rows": 8})}
