from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count, Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from crm.forms import BotLeadForm, CallLogForm, DocumentTemplateForm, InboxMessageForm, ShipmentForm
from crm.models import BotLead, CallLog, Client, Deal, DealStage, DocumentTemplate, InboxMessage, Order, Shipment, Task

from .mixins import CRMLoginRequiredMixin, SearchFilterMixin, scope_queryset_for_user


class InboxView(CRMLoginRequiredMixin, SearchFilterMixin, ListView):
    model = InboxMessage
    template_name = "crm/integrations/inbox.html"
    context_object_name = "messages"
    paginate_by = 30
    search_fields = ["sender_name", "sender_handle", "text", "client__name"]
    filter_fields = {"channel": "channel", "status": "status"}

    def get_queryset(self):
        return self.apply_search_and_filters(InboxMessage.objects.select_related("client", "deal"))


class InboxMessageCreateView(CRMLoginRequiredMixin, CreateView):
    model = InboxMessage
    form_class = InboxMessageForm
    template_name = "crm/form.html"
    success_url = reverse_lazy("crm:inbox")


class ShipmentListView(CRMLoginRequiredMixin, SearchFilterMixin, ListView):
    model = Shipment
    template_name = "crm/integrations/shipments.html"
    context_object_name = "shipments"
    paginate_by = 30
    search_fields = ["tracking_number", "order__number", "order__client__name", "recipient_city"]
    filter_fields = {"status": "status"}

    def get_queryset(self):
        return self.apply_search_and_filters(Shipment.objects.select_related("order", "order__client", "order__owner"))


class ShipmentCreateView(CRMLoginRequiredMixin, CreateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = "crm/form.html"
    success_url = reverse_lazy("crm:shipments")

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get("order"):
            initial["order"] = self.request.GET["order"]
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["order"].queryset = scope_queryset_for_user(Order.objects.all(), self.request.user)
        return form


class BotLeadListView(CRMLoginRequiredMixin, ListView):
    model = BotLead
    template_name = "crm/integrations/bot_leads.html"
    context_object_name = "leads"
    paginate_by = 30


class BotLeadCreateView(CRMLoginRequiredMixin, CreateView):
    model = BotLead
    form_class = BotLeadForm
    template_name = "crm/form.html"
    success_url = reverse_lazy("crm:bot_leads")

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        if form.cleaned_data.get("create_client_and_deal"):
            client = Client.objects.create(
                name=self.object.name,
                phone=self.object.phone,
                email=self.object.email,
                notes=self.object.message,
                owner=self.request.user,
                status=Client.Status.NEW,
            )
            stage = DealStage.objects.filter(is_active=True).first()
            deal = Deal.objects.create(
                title=f"Заявка: {self.object.name}",
                client=client,
                stage=stage,
                owner=self.request.user,
                source=self.object.get_source_display(),
                description=self.object.message,
            )
            self.object.client = client
            self.object.deal = deal
            self.object.is_processed = True
            self.object.save(update_fields=["client", "deal", "is_processed"])
            messages.success(self.request, "Созданы клиент и сделка из заявки чат-бота.")
        return response


class CallLogListView(CRMLoginRequiredMixin, SearchFilterMixin, ListView):
    model = CallLog
    template_name = "crm/integrations/calls.html"
    context_object_name = "calls"
    paginate_by = 30
    search_fields = ["phone", "client__name", "comment"]
    filter_fields = {"status": "status", "direction": "direction"}

    def get_queryset(self):
        return self.apply_search_and_filters(CallLog.objects.select_related("client", "assigned_to"))


class CallLogCreateView(CRMLoginRequiredMixin, CreateView):
    model = CallLog
    form_class = CallLogForm
    template_name = "crm/form.html"
    success_url = reverse_lazy("crm:calls")


class DocumentTemplateListView(CRMLoginRequiredMixin, ListView):
    model = DocumentTemplate
    template_name = "crm/settings/templates.html"
    context_object_name = "templates"


class DocumentTemplateCreateView(CRMLoginRequiredMixin, CreateView):
    model = DocumentTemplate
    form_class = DocumentTemplateForm
    template_name = "crm/form.html"
    success_url = reverse_lazy("crm:document_templates")


class AnalyticsView(CRMLoginRequiredMixin, TemplateView):
    template_name = "crm/analytics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deals = scope_queryset_for_user(Deal.objects.all(), self.request.user)
        tasks = scope_queryset_for_user(Task.objects.all(), self.request.user)
        context["manager_stats"] = (
            User.objects.annotate(deals_count=Count("crm_deals", distinct=True), deals_amount=Sum("crm_deals__amount"), orders_count=Count("crm_orders", distinct=True), orders_total=Sum("crm_orders__total"))
            .filter(deals_count__gt=0)
            .order_by("-deals_amount")
        )
        context["source_stats"] = deals.values("source").annotate(count=Count("id"), amount=Sum("amount")).order_by("-count")
        context["lost_deals"] = deals.filter(stage__is_lost=True).select_related("client", "owner", "stage")
        context["task_stats"] = tasks.values("assigned_to__username", "status").annotate(count=Count("id")).order_by("assigned_to__username")
        return context
