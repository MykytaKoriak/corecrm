from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from crm.forms import OrderFileForm, OrderForm, OrderItemForm
from crm.models import ActivityLog, Order, OrderFile, OrderItem

from .mixins import CRMLoginRequiredMixin, SearchFilterMixin, scope_queryset_for_user


class OrderListView(CRMLoginRequiredMixin, SearchFilterMixin, ListView):
    model = Order
    template_name = "crm/orders/list.html"
    context_object_name = "orders"
    paginate_by = 20
    search_fields = ["number", "client__name"]
    filter_fields = {"payment": "payment_status", "delivery": "delivery_status", "work": "work_status"}

    def get_queryset(self):
        qs = Order.objects.select_related("client", "owner", "deal")
        return self.apply_search_and_filters(qs)


class OrderDetailView(CRMLoginRequiredMixin, DetailView):
    model = Order
    template_name = "crm/orders/detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activity"] = ActivityLog.objects.filter(object_id=str(self.object.pk), content_type__model="order")[:12]
        return context


class OrderCreateView(CRMLoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = "crm/form.html"

    def form_valid(self, form):
        if not form.instance.owner:
            form.instance.owner = self.request.user
        messages.success(self.request, "Заказ создан.")
        return super().form_valid(form)


class OrderUpdateView(CRMLoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "crm/form.html"


class OrderDeleteView(CRMLoginRequiredMixin, DeleteView):
    model = Order
    template_name = "crm/confirm_delete.html"
    success_url = reverse_lazy("crm:orders")


class OrderItemCreateView(CRMLoginRequiredMixin, CreateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = "crm/form.html"

    def dispatch(self, request, *args, **kwargs):
        orders = scope_queryset_for_user(Order.objects.all(), request.user)
        self.order = get_object_or_404(orders, pk=kwargs["order_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.order = self.order
        return super().form_valid(form)

    def get_success_url(self):
        return self.order.get_absolute_url()


class OrderFileCreateView(CRMLoginRequiredMixin, CreateView):
    model = OrderFile
    form_class = OrderFileForm
    template_name = "crm/form.html"

    def dispatch(self, request, *args, **kwargs):
        orders = scope_queryset_for_user(Order.objects.all(), request.user)
        self.order = get_object_or_404(orders, pk=kwargs["order_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.order = self.order
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, "Файл заказа загружен.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.order.get_absolute_url()
