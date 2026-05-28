from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from crm.forms import ClientForm, ContactPersonForm
from crm.models import ActivityLog, Client

from .mixins import CRMLoginRequiredMixin, SearchFilterMixin


class ClientListView(CRMLoginRequiredMixin, SearchFilterMixin, ListView):
    model = Client
    template_name = "crm/clients/list.html"
    context_object_name = "clients"
    paginate_by = 20
    search_fields = ["name", "phone", "email", "telegram", "instagram"]
    filter_fields = {"status": "status", "owner": "owner"}

    def get_queryset(self):
        qs = Client.objects.select_related("owner")
        return self.apply_search_and_filters(qs)


class ClientDetailView(CRMLoginRequiredMixin, DetailView):
    model = Client
    template_name = "crm/clients/detail.html"
    context_object_name = "client"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact_form"] = ContactPersonForm()
        context["activity"] = ActivityLog.objects.filter(object_id=str(self.object.pk), content_type__model="client")[:12]
        return context


class ClientCreateView(CRMLoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "crm/form.html"

    def form_valid(self, form):
        if not form.instance.owner:
            form.instance.owner = self.request.user
        messages.success(self.request, "Клиент создан.")
        return super().form_valid(form)


class ClientUpdateView(CRMLoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "crm/form.html"

    def form_valid(self, form):
        messages.success(self.request, "Клиент обновлен.")
        return super().form_valid(form)


class ClientDeleteView(CRMLoginRequiredMixin, DeleteView):
    model = Client
    template_name = "crm/confirm_delete.html"
    success_url = reverse_lazy("crm:clients")
