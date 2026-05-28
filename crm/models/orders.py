from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse


class Order(models.Model):
    class PaymentStatus(models.TextChoices):
        UNPAID = "unpaid", "Не оплачен"
        PARTIAL = "partial", "Частично"
        PAID = "paid", "Оплачен"

    class DeliveryStatus(models.TextChoices):
        NEW = "new", "Не отправлен"
        IN_TRANSIT = "in_transit", "В пути"
        DELIVERED = "delivered", "Доставлен"
        RETURNED = "returned", "Возврат"

    class WorkStatus(models.TextChoices):
        PROCESSING = "processing", "В обработке"
        IN_WORK = "in_work", "В работе"
        READY = "ready", "Готов"
        CLOSED = "closed", "Закрыт"

    number = models.CharField("Номер", max_length=40, unique=True, blank=True)
    client = models.ForeignKey("crm.Client", verbose_name="Клиент", on_delete=models.PROTECT, related_name="orders")
    deal = models.OneToOneField("crm.Deal", verbose_name="Сделка", null=True, blank=True, on_delete=models.SET_NULL, related_name="order")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Ответственный", null=True, blank=True, on_delete=models.SET_NULL, related_name="crm_orders")
    payment_status = models.CharField("Оплата", max_length=16, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    delivery_status = models.CharField("Доставка", max_length=16, choices=DeliveryStatus.choices, default=DeliveryStatus.NEW)
    work_status = models.CharField("Работа", max_length=16, choices=WorkStatus.choices, default=WorkStatus.PROCESSING)
    discount = models.DecimalField("Скидка", max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField("Итого", max_digits=12, decimal_places=2, default=Decimal("0.00"))
    comments = models.TextField("Комментарии", blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.number:
            self.number = f"ORD-{self.pk:06d}"
            super().save(update_fields=["number"])

    def recalculate_total(self):
        total = sum(item.line_total for item in self.items.all()) - self.discount
        self.total = max(Decimal("0.00"), total)
        self.save(update_fields=["total", "updated_at"])

    def __str__(self):
        return self.number or f"Заказ #{self.pk}"

    def get_absolute_url(self):
        return reverse("crm:order_detail", kwargs={"pk": self.pk})


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name="Заказ", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("crm.Product", verbose_name="Товар", null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField("Название", max_length=255)
    quantity = models.DecimalField("Количество", max_digits=12, decimal_places=2, default=Decimal("1.00"))
    price = models.DecimalField("Цена", max_digits=12, decimal_places=2, default=Decimal("0.00"))
    discount = models.DecimalField("Скидка", max_digits=12, decimal_places=2, default=Decimal("0.00"))
    line_total = models.DecimalField("Сумма", max_digits=12, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def save(self, *args, **kwargs):
        if self.product and not self.name:
            self.name = self.product.name
        self.line_total = max(Decimal("0.00"), (self.quantity * self.price) - self.discount)
        super().save(*args, **kwargs)
        self.order.recalculate_total()

    def __str__(self):
        return self.name
