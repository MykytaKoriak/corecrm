from django import forms

from crm.models import Task

from .base import StyledFormMixin


class TaskForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "assigned_to", "client", "deal", "deadline", "status", "priority"]
        widgets = {
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }
