from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Notification(models.Model):
    class Kind(models.TextChoices):
        INFO = "info", "Информация"
        TASK = "task", "Задача"
        DEAL = "deal", "Сделка"
        ORDER = "order", "Заказ"
        INTEGRATION = "integration", "Интеграция"
        WARNING = "warning", "Важно"

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Получатель", on_delete=models.CASCADE, related_name="crm_notifications")
    title = models.CharField("Заголовок", max_length=255)
    message = models.TextField("Сообщение", blank=True)
    kind = models.CharField("Тип", max_length=24, choices=Kind.choices, default=Kind.INFO)
    link = models.CharField("Ссылка", max_length=255, blank=True)
    read_at = models.DateTimeField("Прочитано", null=True, blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ["-created_at"]

    @property
    def is_read(self):
        return self.read_at is not None

    def mark_read(self):
        if not self.read_at:
            self.read_at = timezone.now()
            self.save(update_fields=["read_at"])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("crm:notifications")
