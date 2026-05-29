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


class OrderFile(models.Model):
    order = models.ForeignKey(Order, verbose_name="Заказ", on_delete=models.CASCADE, related_name="files")
    file = models.FileField("Файл", upload_to="orders/%Y/%m/")
    title = models.CharField("Название", max_length=180, blank=True)
    comment = models.CharField("Комментарий", max_length=255, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Загрузил", null=True, blank=True, on_delete=models.SET_NULL)
    uploaded_at = models.DateTimeField("Загружен", auto_now_add=True)

    class Meta:
        verbose_name = "Файл заказа"
        verbose_name_plural = "Файлы заказов"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title or self.file.name


class Shipment(models.Model):
    class Provider(models.TextChoices):
        NOVA_POSHTA = "nova_poshta", "Новая Почта"

    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        CREATED = "created", "ТТН создана"
        IN_TRANSIT = "in_transit", "В пути"
        DELIVERED = "delivered", "Доставлено"
        RETURNED = "returned", "Возврат"

    order = models.ForeignKey(Order, verbose_name="Заказ", on_delete=models.CASCADE, related_name="shipments")
    provider = models.CharField("Служба", max_length=32, choices=Provider.choices, default=Provider.NOVA_POSHTA)
    tracking_number = models.CharField("ТТН", max_length=80, blank=True)
    status = models.CharField("Статус", max_length=24, choices=Status.choices, default=Status.DRAFT)
    recipient_city = models.CharField("Город", max_length=160, blank=True)
    recipient_warehouse = models.CharField("Отделение", max_length=255, blank=True)
    api_payload = models.JSONField("Данные API", default=dict, blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Отправление"
        verbose_name_plural = "Отправления"
        ordering = ["-updated_at"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.tracking_number:
            self.tracking_number = f"NP-{self.pk:08d}"
            super().save(update_fields=["tracking_number"])

    def __str__(self):
        return self.tracking_number or f"Отправление #{self.pk}"
