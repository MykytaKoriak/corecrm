from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from crm.forms import ClientFileForm, ClientForm, ContactPersonForm
from crm.models import ActivityLog, Client, ClientFile, ContactPerson

from .mixins import CRMLoginRequiredMixin, SearchFilterMixin, scope_queryset_for_user


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

    def get_initial(self):
        initial = super().get_initial()
        initial["owner"] = self.request.user.pk
        return initial

    def form_valid(self, form):
        if not form.instance.owner:
            form.instance.owner = self.request.user
        response = super().form_valid(form)
        if form.instance.primary_contact_name and not form.instance.contacts.exists():
            ContactPerson.objects.create(client=form.instance, name=form.instance.primary_contact_name, phone=form.instance.phone, email=form.instance.email, is_primary=True)
        messages.success(self.request, "Клиент создан.")
        return response


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


class ClientFileCreateView(CRMLoginRequiredMixin, CreateView):
    model = ClientFile
    form_class = ClientFileForm
    template_name = "crm/form.html"

    def dispatch(self, request, *args, **kwargs):
        clients = scope_queryset_for_user(Client.objects.all(), request.user)
        self.client = get_object_or_404(clients, pk=kwargs["client_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.client = self.client
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, "Файл клиента загружен.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.client.get_absolute_url()


class ContactPersonCreateView(CRMLoginRequiredMixin, CreateView):
    model = ContactPerson
    form_class = ContactPersonForm
    template_name = "crm/form.html"

    def dispatch(self, request, *args, **kwargs):
        clients = scope_queryset_for_user(Client.objects.all(), request.user)
        self.client = get_object_or_404(clients, pk=kwargs["client_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.client = self.client
        messages.success(self.request, "Контакт добавлен.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.client.get_absolute_url()
