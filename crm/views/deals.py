from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from crm.forms import DealForm, DealItemForm
from crm.models import ActivityLog, Deal, DealItem, DealStage, Order, OrderItem

from .mixins import CRMLoginRequiredMixin, SearchFilterMixin, scope_queryset_for_user


class DealPipelineView(CRMLoginRequiredMixin, ListView):
    model = DealStage
    template_name = "crm/deals/pipeline.html"
    context_object_name = "stages"

    def get_queryset(self):
        deals = scope_queryset_for_user(Deal.objects.select_related("client", "owner"), self.request.user)
        return DealStage.objects.filter(is_active=True).prefetch_related(Prefetch("deals", queryset=deals))


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
        initial["owner"] = self.request.user.pk
        if self.request.GET.get("client"):
            initial["client"] = self.request.GET["client"]
        return initial

    def form_valid(self, form):
        if not form.instance.owner:
            form.instance.owner = self.request.user
        if not form.instance.stage:
            form.instance.stage = DealStage.objects.filter(is_active=True).first()
        if not form.instance.title and form.instance.client_id:
            form.instance.title = form.instance.default_title()
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


class DealItemCreateView(CRMLoginRequiredMixin, CreateView):
    model = DealItem
    form_class = DealItemForm
    template_name = "crm/form.html"

    def dispatch(self, request, *args, **kwargs):
        deals = scope_queryset_for_user(Deal.objects.all(), request.user)
        self.deal = get_object_or_404(deals, pk=kwargs["deal_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.deal = self.deal
        messages.success(self.request, "Товар добавлен в сделку.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.deal.get_absolute_url()


@require_POST
@login_required
def update_deal_stage(request, pk):
    deals = scope_queryset_for_user(Deal.objects.all(), request.user)
    deal = get_object_or_404(deals, pk=pk)
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
    deals = scope_queryset_for_user(Deal.objects.select_related("client", "owner"), request.user)
    deal = get_object_or_404(deals, pk=pk)
    if hasattr(deal, "order"):
        messages.info(request, "Заказ по этой сделке уже создан.")
        return redirect(deal.order.get_absolute_url())
    order = Order.objects.create(client=deal.client, deal=deal, owner=deal.owner, total=deal.amount, comments=deal.description)
    for item in deal.items.all():
        OrderItem.objects.create(order=order, product=item.product, name=item.name, quantity=item.quantity, price=item.price, discount=item.discount)
    messages.success(request, f"Создан заказ {order.number}.")
    return redirect(order.get_absolute_url())
