from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from crm.forms import ProductForm
from crm.models import Product

from .mixins import CRMLoginRequiredMixin, SearchFilterMixin


class ProductListView(CRMLoginRequiredMixin, SearchFilterMixin, ListView):
    model = Product
    template_name = "crm/products/list.html"
    context_object_name = "products"
    paginate_by = 20
    search_fields = ["name", "sku", "category"]
    filter_fields = {"status": "status", "category": "category"}

    def get_queryset(self):
        return self.apply_search_and_filters(Product.objects.all())


class ProductDetailView(CRMLoginRequiredMixin, DetailView):
    model = Product
    template_name = "crm/products/detail.html"
    context_object_name = "product"


class ProductCreateView(CRMLoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "crm/form.html"


class ProductUpdateView(CRMLoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "crm/form.html"


class ProductDeleteView(CRMLoginRequiredMixin, DeleteView):
    model = Product
    template_name = "crm/confirm_delete.html"
    success_url = reverse_lazy("crm:products")
