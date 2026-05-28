from django.contrib.auth.mixins import LoginRequiredMixin


class CRMLoginRequiredMixin(LoginRequiredMixin):
    login_url = "crm:login"


class SearchFilterMixin:
    search_fields = []
    filter_fields = {}

    def apply_search_and_filters(self, queryset):
        query = self.request.GET.get("q", "").strip()
        if query and self.search_fields:
            combined = None
            for field in self.search_fields:
                condition = {f"{field}__icontains": query}
                match = queryset.model.objects.filter(**condition)
                combined = match if combined is None else combined | match
            queryset = queryset.filter(pk__in=combined.values("pk")) if combined is not None else queryset
        for param, field in self.filter_fields.items():
            value = self.request.GET.get(param)
            if value:
                queryset = queryset.filter(**{field: value})
        return queryset
