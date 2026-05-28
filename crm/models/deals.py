from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse


class DealStage(models.Model):
    name = models.CharField("Название", max_length=120, unique=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    color = models.CharField("Цвет", max_length=20, default="#64748b")
    is_won = models.BooleanField("Успешный финал", default=False)
    is_lost = models.BooleanField("Отказ", default=False)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Этап сделки"
        verbose_name_plural = "Этапы сделок"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Deal(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Низкий"
        MEDIUM = "medium", "Средний"
        HIGH = "high", "Высокий"

    title = models.CharField("Название", max_length=255)
    client = models.ForeignKey("crm.Client", verbose_name="Клиент", on_delete=models.CASCADE, related_name="deals")
    stage = models.ForeignKey(DealStage, verbose_name="Этап", null=True, blank=True, on_delete=models.SET_NULL, related_name="deals")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Ответственный", null=True, blank=True, on_delete=models.SET_NULL, related_name="crm_deals")
    source = models.CharField("Источник", max_length=120, blank=True)
    priority = models.CharField("Приоритет", max_length=16, choices=Priority.choices, default=Priority.MEDIUM)
    amount = models.DecimalField("Сумма", max_digits=12, decimal_places=2, default=Decimal("0.00"))
    probability = models.PositiveSmallIntegerField("Вероятность, %", default=20)
    expected_close_date = models.DateField("Ожидаемое закрытие", null=True, blank=True)
    description = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"
        ordering = ["stage__order", "-updated_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("crm:deal_detail", kwargs={"pk": self.pk})
