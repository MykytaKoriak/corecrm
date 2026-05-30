from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from crm.forms import ProductForm
from crm.models import Product

from .mixins import CRMLoginRequiredMixin, ProductEditRequiredMixin, SearchFilterMixin


class ProductListView(CRMLoginRequiredMixin, SearchFilterMixin, ListView):
    model = Product
    template_name = "crm/products/list.html"
    context_object_name = "products"
    paginate_by = 20
    search_fields = ["name", "sku", "category"]
    filter_fields = {"status": "status", "category": "category"}

    def get_queryset(self):
        return self.apply_search_and_filters(Product.objects.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Product.objects.exclude(category="").values("category").annotate(count=Count("id")).order_by("category")
        context["can_edit_products"] = self.can_edit_products()
        return context


class ProductDetailView(CRMLoginRequiredMixin, DetailView):
    model = Product
    template_name = "crm/products/detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_edit_products"] = self.can_edit_products()
        return context


class ProductCreateView(ProductEditRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "crm/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_options"] = Product.objects.exclude(category="").values_list("category", flat=True).distinct().order_by("category")
        return context


class ProductUpdateView(ProductEditRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "crm/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_options"] = Product.objects.exclude(category="").values_list("category", flat=True).distinct().order_by("category")
        return context


class ProductDeleteView(ProductEditRequiredMixin, DeleteView):
    model = Product
    template_name = "crm/confirm_delete.html"
    success_url = reverse_lazy("crm:products")


class ProductCategoryListView(CRMLoginRequiredMixin, ListView):
    model = Product
    template_name = "crm/products/categories.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = Product.objects.exclude(category="").order_by("category", "name")
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Product.objects.exclude(category="").values("category").annotate(count=Count("id")).order_by("category")
        context["selected_category"] = self.request.GET.get("category", "")
        return context
