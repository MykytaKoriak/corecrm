from django.db import models


class IntegrationPlaceholder(models.Model):
    class Provider(models.TextChoices):
        NOVA_POSHTA = "nova_poshta", "Новая Почта"
        TELEGRAM = "telegram", "Telegram"
        INSTAGRAM = "instagram", "Instagram"
        TELEPHONY = "telephony", "Телефония"

    provider = models.CharField("Провайдер", max_length=32, choices=Provider.choices, unique=True)
    is_enabled = models.BooleanField("Включено", default=False)
    config = models.JSONField("Конфигурация", default=dict, blank=True)
    notes = models.TextField("Заметки", blank=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Интеграция"
        verbose_name_plural = "Интеграции"

    def __str__(self):
        return self.get_provider_display()
