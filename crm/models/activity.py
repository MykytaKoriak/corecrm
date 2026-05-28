from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ActivityLog(models.Model):
    class Action(models.TextChoices):
        CREATED = "created", "Создание"
        UPDATED = "updated", "Изменение"
        DELETED = "deleted", "Удаление"
        STATUS_CHANGED = "status_changed", "Изменение статуса"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Пользователь", null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField("Действие", max_length=32, choices=Action.choices)
    content_type = models.ForeignKey(ContentType, verbose_name="Тип объекта", null=True, blank=True, on_delete=models.SET_NULL)
    object_id = models.CharField("ID объекта", max_length=64, blank=True)
    object_repr = models.CharField("Объект", max_length=255)
    changes = models.JSONField("Изменения", default=dict, blank=True)
    created_at = models.DateTimeField("Дата", auto_now_add=True)

    class Meta:
        verbose_name = "История действия"
        verbose_name_plural = "История действий"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_action_display()}: {self.object_repr}"
