from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from crm.models import Deal, Notification, Task


def notification_context(request):
    if not request.user.is_authenticated:
        return {"unread_notifications_count": 0, "latest_notifications": []}
    qs = request.user.crm_notifications.filter(read_at__isnull=True)
    return {"unread_notifications_count": qs.count(), "latest_notifications": qs[:5]}


def notify_user(user, title, message="", kind=Notification.Kind.INFO, link=""):
    if not user:
        return None
    return Notification.objects.create(recipient=user, title=title, message=message, kind=kind, link=link)


@receiver(post_save, sender=Task)
def notify_task_assignee(sender, instance, created, **kwargs):
    if created and instance.assigned_to:
        notify_user(
            instance.assigned_to,
            f"Новая задача: {instance.title}",
            instance.description,
            Notification.Kind.TASK,
            instance.get_absolute_url(),
        )


@receiver(post_save, sender=Deal)
def notify_new_deal(sender, instance, created, **kwargs):
    if created and instance.owner:
        notify_user(
            instance.owner,
            f"Новая сделка: {instance.title}",
            f"Клиент: {instance.client}",
            Notification.Kind.DEAL,
            instance.get_absolute_url(),
        )


def notify_overdue_tasks_now():
    now = timezone.now()
    tasks = Task.objects.filter(
        status=Task.Status.ACTIVE,
        deadline__lt=now,
        overdue_notified_at__isnull=True,
        assigned_to__isnull=False,
    )
    count = 0
    for task in tasks:
        notify_user(
            task.assigned_to,
            f"Просрочена задача: {task.title}",
            f"Дедлайн был {task.deadline:%d.%m.%Y %H:%M}",
            Notification.Kind.WARNING,
            task.get_absolute_url(),
        )
        task.overdue_notified_at = now
        task.save(update_fields=["overdue_notified_at"])
        count += 1
    return count
