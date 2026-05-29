from django import forms

from crm.models import Client, ClientFile, ContactPerson

from .base import StyledFormMixin


class ClientForm(StyledFormMixin, forms.ModelForm):
    extra_phones_text = forms.CharField(label="Дополнительные телефоны", required=False, help_text="Через запятую")
    extra_emails_text = forms.CharField(label="Дополнительные email", required=False, help_text="Через запятую")
    tags_text = forms.CharField(label="Теги", required=False, help_text="Через запятую")

    class Meta:
        model = Client
        fields = [
            "name",
            "client_type",
            "status",
            "owner",
            "phone",
            "extra_phones_text",
            "email",
            "extra_emails_text",
            "telegram",
            "instagram",
            "delivery_address",
            "legal_address",
            "tags_text",
            "notes",
        ]
        widgets = {
            "delivery_address": forms.Textarea(attrs={"rows": 2}),
            "legal_address": forms.Textarea(attrs={"rows": 2}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["extra_phones_text"].initial = ", ".join(self.instance.extra_phones)
            self.fields["extra_emails_text"].initial = ", ".join(self.instance.extra_emails)
            self.fields["tags_text"].initial = ", ".join(self.instance.tags)

    def clean(self):
        cleaned = super().clean()
        for source, target in (
            ("extra_phones_text", "extra_phones"),
            ("extra_emails_text", "extra_emails"),
            ("tags_text", "tags"),
        ):
            cleaned[target] = [item.strip() for item in cleaned.get(source, "").split(",") if item.strip()]
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.extra_phones = self.cleaned_data["extra_phones"]
        instance.extra_emails = self.cleaned_data["extra_emails"]
        instance.tags = self.cleaned_data["tags"]
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class ContactPersonForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = ["name", "position", "phone", "email", "telegram", "is_primary"]


class ClientFileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ["title", "file", "comment"]
