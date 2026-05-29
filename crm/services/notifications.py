from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from crm.models import CallLog, Deal, InboxMessage, Notification, Shipment, Task


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


@receiver(post_save, sender=InboxMessage)
def notify_inbox_message(sender, instance, created, **kwargs):
    if created and instance.client and instance.client.owner:
        notify_user(
            instance.client.owner,
            f"Новое сообщение: {instance.sender_name or instance.sender_handle}",
            instance.text[:240],
            Notification.Kind.INFO,
            instance.get_absolute_url(),
        )


@receiver(post_save, sender=Shipment)
def notify_returned_shipment(sender, instance, created, **kwargs):
    if instance.status == Shipment.Status.RETURNED and instance.order.owner:
        notify_user(
            instance.order.owner,
            f"Возврат по заказу {instance.order.number}",
            f"Отправление {instance.tracking_number} отмечено как возврат.",
            Notification.Kind.WARNING,
            instance.order.get_absolute_url(),
        )


@receiver(post_save, sender=CallLog)
def create_task_for_missed_call(sender, instance, created, **kwargs):
    if not created or instance.status != CallLog.Status.MISSED or instance.task_created:
        return
    assignee = instance.assigned_to or (instance.client.owner if instance.client else None)
    if not assignee:
        return
    task = Task.objects.create(
        title=f"Перезвонить: {instance.phone}",
        description=instance.comment or "Автоматическая задача по пропущенному звонку.",
        assigned_to=assignee,
        created_by=assignee,
        client=instance.client,
        priority=Task.Priority.HIGH,
    )
    instance.task_created = True
    instance.save(update_fields=["task_created"])
    notify_user(
        assignee,
        f"Пропущенный звонок: {instance.phone}",
        f"Создана задача: {task.title}",
        Notification.Kind.WARNING,
        task.get_absolute_url(),
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
