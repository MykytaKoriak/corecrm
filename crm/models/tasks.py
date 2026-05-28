from django.conf import settings
from django.db import models
from django.urls import reverse


class Task(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активна"
        DONE = "done", "Выполнена"
        CANCELED = "canceled", "Отменена"

    class Priority(models.TextChoices):
        LOW = "low", "Низкий"
        MEDIUM = "medium", "Средний"
        HIGH = "high", "Высокий"

    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Ответственный", null=True, blank=True, on_delete=models.SET_NULL, related_name="crm_tasks")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Поставил", null=True, blank=True, on_delete=models.SET_NULL, related_name="crm_created_tasks")
    client = models.ForeignKey("crm.Client", verbose_name="Клиент", null=True, blank=True, on_delete=models.SET_NULL, related_name="tasks")
    deal = models.ForeignKey("crm.Deal", verbose_name="Сделка", null=True, blank=True, on_delete=models.SET_NULL, related_name="tasks")
    deadline = models.DateTimeField("Дедлайн", null=True, blank=True)
    status = models.CharField("Статус", max_length=16, choices=Status.choices, default=Status.ACTIVE)
    priority = models.CharField("Приоритет", max_length=16, choices=Priority.choices, default=Priority.MEDIUM)
    overdue_notified_at = models.DateTimeField("Уведомление о просрочке", null=True, blank=True)
    completed_at = models.DateTimeField("Выполнена", null=True, blank=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["status", "deadline", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("crm:task_detail", kwargs={"pk": self.pk})
