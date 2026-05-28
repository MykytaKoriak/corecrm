from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from crm.forms import DealForm
from crm.models import ActivityLog, Deal, DealStage, Order

from .mixins import CRMLoginRequiredMixin, SearchFilterMixin


class DealPipelineView(CRMLoginRequiredMixin, ListView):
    model = DealStage
    template_name = "crm/deals/pipeline.html"
    context_object_name = "stages"

    def get_queryset(self):
        return DealStage.objects.filter(is_active=True).prefetch_related("deals__client", "deals__owner")


class DealListView(CRMLoginRequiredMixin, SearchFilterMixin, ListView):
    model = Deal
    template_name = "crm/deals/list.html"
    context_object_name = "deals"
    paginate_by = 20
    search_fields = ["title", "client__name", "source"]
    filter_fields = {"stage": "stage", "priority": "priority", "owner": "owner"}

    def get_queryset(self):
        qs = Deal.objects.select_related("client", "stage", "owner")
        return self.apply_search_and_filters(qs)


class DealDetailView(CRMLoginRequiredMixin, DetailView):
    model = Deal
    template_name = "crm/deals/detail.html"
    context_object_name = "deal"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activity"] = ActivityLog.objects.filter(object_id=str(self.object.pk), content_type__model="deal")[:12]
        return context


class DealCreateView(CRMLoginRequiredMixin, CreateView):
    model = Deal
    form_class = DealForm
    template_name = "crm/form.html"

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get("client"):
            initial["client"] = self.request.GET["client"]
        return initial

    def form_valid(self, form):
        if not form.instance.owner:
            form.instance.owner = self.request.user
        if not form.instance.stage:
            form.instance.stage = DealStage.objects.filter(is_active=True).first()
        messages.success(self.request, "Сделка создана.")
        return super().form_valid(form)


class DealUpdateView(CRMLoginRequiredMixin, UpdateView):
    model = Deal
    form_class = DealForm
    template_name = "crm/form.html"


class DealDeleteView(CRMLoginRequiredMixin, DeleteView):
    model = Deal
    template_name = "crm/confirm_delete.html"
    success_url = reverse_lazy("crm:deals")


@require_POST
@login_required
def update_deal_stage(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    stage = get_object_or_404(DealStage, pk=request.POST.get("stage"))
    deal.stage = stage
    deal.save(update_fields=["stage", "updated_at"])
    if request.headers.get("HX-Request"):
        return redirect("crm:deals")
    return redirect("crm:deal_detail", pk=pk)


@require_POST
@login_required
@transaction.atomic
def create_order_from_deal(request, pk):
    deal = get_object_or_404(Deal.objects.select_related("client", "owner"), pk=pk)
    if hasattr(deal, "order"):
        messages.info(request, "Заказ по этой сделке уже создан.")
        return redirect(deal.order.get_absolute_url())
    order = Order.objects.create(client=deal.client, deal=deal, owner=deal.owner, total=deal.amount, comments=deal.description)
    messages.success(request, f"Создан заказ {order.number}.")
    return redirect(order.get_absolute_url())
