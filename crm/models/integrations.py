from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


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


class InboxMessage(models.Model):
    class Channel(models.TextChoices):
        TELEGRAM = "telegram", "Telegram"
        INSTAGRAM = "instagram", "Instagram"
        TELEPHONY = "telephony", "Телефония"
        MANUAL = "manual", "Вручную"

    class Status(models.TextChoices):
        NEW = "new", "Новое"
        LINKED = "linked", "Привязано"
        PROCESSED = "processed", "Обработано"

    channel = models.CharField("Канал", max_length=32, choices=Channel.choices)
    sender_name = models.CharField("Отправитель", max_length=160, blank=True)
    sender_handle = models.CharField("Контакт", max_length=160, blank=True)
    text = models.TextField("Сообщение")
    client = models.ForeignKey("crm.Client", verbose_name="Клиент", null=True, blank=True, on_delete=models.SET_NULL, related_name="messages")
    deal = models.ForeignKey("crm.Deal", verbose_name="Сделка", null=True, blank=True, on_delete=models.SET_NULL, related_name="messages")
    status = models.CharField("Статус", max_length=24, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField("Получено", auto_now_add=True)

    class Meta:
        verbose_name = "Сообщение inbox"
        verbose_name_plural = "Сообщения inbox"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.client and self.sender_handle:
            from crm.models import Client

            handle = self.sender_handle.strip().lower()
            self.client = (
                Client.objects.filter(telegram__iexact=handle).first()
                or Client.objects.filter(instagram__iexact=handle).first()
                or Client.objects.filter(phone__icontains=handle).first()
                or Client.objects.filter(email__iexact=handle).first()
            )
        if self.client and self.status == self.Status.NEW:
            self.status = self.Status.LINKED
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_channel_display()}: {self.sender_name or self.sender_handle}"

    def get_absolute_url(self):
        return reverse("crm:inbox")


class BotLead(models.Model):
    class Source(models.TextChoices):
        TELEGRAM = "telegram", "Telegram bot"
        INSTAGRAM = "instagram", "Instagram"
        WEBSITE = "website", "Сайт"

    source = models.CharField("Источник", max_length=32, choices=Source.choices, default=Source.TELEGRAM)
    name = models.CharField("Имя", max_length=180)
    phone = models.CharField("Телефон", max_length=40, blank=True)
    email = models.EmailField("Email", blank=True)
    message = models.TextField("Сообщение", blank=True)
    client = models.ForeignKey("crm.Client", verbose_name="Созданный клиент", null=True, blank=True, on_delete=models.SET_NULL)
    deal = models.ForeignKey("crm.Deal", verbose_name="Созданная сделка", null=True, blank=True, on_delete=models.SET_NULL)
    is_processed = models.BooleanField("Обработан", default=False)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка чат-бота"
        verbose_name_plural = "Заявки чат-ботов"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} · {self.get_source_display()}"


class CallLog(models.Model):
    class Direction(models.TextChoices):
        INCOMING = "incoming", "Входящий"
        OUTGOING = "outgoing", "Исходящий"

    class Status(models.TextChoices):
        ANSWERED = "answered", "Принят"
        MISSED = "missed", "Пропущен"

    direction = models.CharField("Направление", max_length=16, choices=Direction.choices, default=Direction.INCOMING)
    status = models.CharField("Статус", max_length=16, choices=Status.choices, default=Status.ANSWERED)
    phone = models.CharField("Телефон", max_length=40)
    client = models.ForeignKey("crm.Client", verbose_name="Клиент", null=True, blank=True, on_delete=models.SET_NULL, related_name="calls")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Ответственный", null=True, blank=True, on_delete=models.SET_NULL)
    recording = models.FileField("Запись звонка", upload_to="calls/%Y/%m/", blank=True)
    comment = models.TextField("Комментарий", blank=True)
    task_created = models.BooleanField("Задача создана", default=False)
    called_at = models.DateTimeField("Дата звонка", default=timezone.now)

    class Meta:
        verbose_name = "Звонок"
        verbose_name_plural = "Звонки"
        ordering = ["-called_at"]

    def __str__(self):
        return f"{self.get_status_display()} · {self.phone}"
