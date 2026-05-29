from django.views.generic import TemplateView

from crm.models import ActivityLog, CustomField, DealStage, DocumentTemplate, IntegrationPlaceholder

from .mixins import CRMLoginRequiredMixin


class SettingsView(CRMLoginRequiredMixin, TemplateView):
    template_name = "crm/settings/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deal_stages"] = DealStage.objects.all()
        context["custom_fields"] = CustomField.objects.all()
        context["integrations"] = IntegrationPlaceholder.objects.all()
        context["document_templates"] = DocumentTemplate.objects.all()
        context["activity"] = ActivityLog.objects.select_related("user", "content_type")[:20]
        return context
