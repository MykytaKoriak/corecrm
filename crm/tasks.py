from celery import shared_task

from crm.services.notifications import notify_overdue_tasks_now


@shared_task
def notify_overdue_tasks():
    return notify_overdue_tasks_now()
