from django.contrib.auth import views as auth_views
from django.db.models import Count, Sum
from django.utils import timezone
from django.views.generic import TemplateView

from crm.models import ActivityLog, Client, Deal, Notification, Order, Task

from .mixins import CRMLoginRequiredMixin, scope_queryset_for_user


class LoginView(auth_views.LoginView):
    template_name = "crm/auth/login.html"
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    pass


class DashboardView(CRMLoginRequiredMixin, TemplateView):
    template_name = "crm/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        clients = scope_queryset_for_user(Client.objects.all(), self.request.user)
        deals = scope_queryset_for_user(Deal.objects.all(), self.request.user)
        orders = scope_queryset_for_user(Order.objects.all(), self.request.user)
        tasks = scope_queryset_for_user(Task.objects.all(), self.request.user)
        context.update(
            {
                "clients_count": clients.count(),
                "deals_count": deals.count(),
                "open_orders_count": orders.exclude(work_status=Order.WorkStatus.CLOSED).count(),
                "sales_total": orders.aggregate(total=Sum("total"))["total"] or 0,
                "new_deals": deals.select_related("client", "stage", "owner").order_by("-created_at")[:6],
                "overdue_tasks": tasks.filter(status=Task.Status.ACTIVE, deadline__lt=now).select_related("assigned_to")[:6],
                "active_orders": orders.exclude(work_status=Order.WorkStatus.CLOSED).select_related("client")[:6],
                "notifications": Notification.objects.filter(recipient=self.request.user, read_at__isnull=True)[:6],
                "deal_stats": deals.values("stage__name", "stage__color").annotate(count=Count("id"), amount=Sum("amount")).order_by("stage__order"),
                "activity": ActivityLog.objects.select_related("user", "content_type")[:8],
            }
        )
        return context
