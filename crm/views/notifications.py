from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from crm.models import Notification

from .mixins import CRMLoginRequiredMixin


class NotificationListView(CRMLoginRequiredMixin, ListView):
    model = Notification
    template_name = "crm/notifications/list.html"
    context_object_name = "notifications"
    paginate_by = 30

    def get_queryset(self):
        qs = Notification.objects.filter(recipient=self.request.user)
        if self.request.GET.get("status") == "unread":
            qs = qs.filter(read_at__isnull=True)
        return qs


@require_POST
@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.mark_read()
    return redirect(request.POST.get("next") or "crm:notifications")


@require_POST
@login_required
def mark_all_notifications_read(request):
    Notification.objects.filter(recipient=request.user, read_at__isnull=True).update(read_at=timezone.now())
    return redirect("crm:notifications")
