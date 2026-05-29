from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


def scope_queryset_for_user(queryset, user):
    role = getattr(getattr(user, "profile", None), "role", "")
    model_name = queryset.model.__name__
    field_names = {field.name for field in queryset.model._meta.get_fields()}

    if user.is_superuser or role in {"admin", "director"}:
        return queryset

    if role == "manager":
        if "owner" in field_names:
            return queryset.filter(owner=user)
        if model_name == "Task":
            return queryset.filter(assigned_to=user)
        if model_name == "ClientFile":
            return queryset.filter(client__owner=user)
        if model_name == "DealItem":
            return queryset.filter(deal__owner=user)
        if model_name in {"OrderItem", "OrderFile", "Shipment"}:
            return queryset.filter(order__owner=user)
        if model_name == "InboxMessage":
            return queryset.filter(Q(client__owner=user) | Q(client__isnull=True))
        if model_name == "BotLead":
            return queryset.filter(Q(client__owner=user) | Q(client__isnull=True))
        if model_name == "CallLog":
            return queryset.filter(Q(assigned_to=user) | Q(client__owner=user))

    if role == "production":
        if model_name == "Order":
            return queryset.exclude(work_status="closed")
        if model_name in {"OrderItem", "OrderFile", "Shipment"}:
            return queryset.exclude(order__work_status="closed")
        if model_name in {"Product", "Task"}:
            return queryset
        if "owner" in field_names:
            return queryset.none()

    return queryset


class CRMLoginRequiredMixin(LoginRequiredMixin):
    login_url = "crm:login"

    def user_role(self):
        return getattr(getattr(self.request.user, "profile", None), "role", "")

    def scope_queryset(self, queryset):
        return scope_queryset_for_user(queryset, self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.scope_queryset(queryset)


class SearchFilterMixin:
    search_fields = []
    filter_fields = {}

    def apply_search_and_filters(self, queryset):
        queryset = self.scope_queryset(queryset)
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

    def scope_queryset(self, queryset):
        return scope_queryset_for_user(queryset, self.request.user)
