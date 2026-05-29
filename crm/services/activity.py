from threading import local

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from crm.models import ActivityLog

_state = local()

TRACKED_MODELS = {
    "Client",
    "ClientFile",
    "ContactPerson",
    "Deal",
    "DealItem",
    "Order",
    "OrderFile",
    "OrderItem",
    "Product",
    "Task",
    "Notification",
    "CustomField",
    "DocumentTemplate",
    "IntegrationPlaceholder",
    "InboxMessage",
    "BotLead",
    "CallLog",
    "Shipment",
}
STATUS_FIELDS = {"status", "stage", "payment_status", "delivery_status", "work_status"}


def get_current_user():
    return getattr(_state, "user", None)


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _state.user = request.user if request.user.is_authenticated else None
        try:
            return self.get_response(request)
        finally:
            _state.user = None


def should_track(sender):
    return sender.__name__ in TRACKED_MODELS


@receiver(pre_save)
def remember_previous(sender, instance, **kwargs):
    if not should_track(sender) or not instance.pk:
        return
    try:
        instance._crm_previous = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        instance._crm_previous = None


@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    if not should_track(sender):
        return
    previous = getattr(instance, "_crm_previous", None)
    action = ActivityLog.Action.CREATED if created else ActivityLog.Action.UPDATED
    changes = {}
    if previous:
        for field in sender._meta.fields:
            name = field.name
            old = getattr(previous, name)
            new = getattr(instance, name)
            if old != new:
                changes[name] = {"from": str(old), "to": str(new)}
        if STATUS_FIELDS.intersection(changes):
            action = ActivityLog.Action.STATUS_CHANGED
    ActivityLog.objects.create(
        user=get_current_user(),
        action=action,
        content_type=ContentType.objects.get_for_model(sender),
        object_id=str(instance.pk),
        object_repr=str(instance),
        changes=changes,
    )


@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if not should_track(sender):
        return
    ActivityLog.objects.create(
        user=get_current_user(),
        action=ActivityLog.Action.DELETED,
        content_type=ContentType.objects.get_for_model(sender),
        object_id=str(instance.pk),
        object_repr=str(instance),
    )


@receiver(post_save, sender=get_user_model())
def ensure_profile(sender, instance, created, **kwargs):
    if created:
        from crm.models import Profile

        Profile.objects.get_or_create(user=instance)
