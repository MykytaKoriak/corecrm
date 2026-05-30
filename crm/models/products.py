from decimal import Decimal

from django.db import models
from django.urls import reverse


class Product(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активен"
        DRAFT = "draft", "Черновик"
        ARCHIVED = "archived", "Архив"

    name = models.CharField("Название", max_length=255)
    sku = models.CharField("Артикул", max_length=80, unique=True)
    category = models.CharField("Категория", max_length=140, blank=True)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Фото", upload_to="products/%Y/%m/", blank=True)
    price = models.DecimalField("Цена продажи", max_digits=12, decimal_places=2, default=Decimal("0.00"))
    cost = models.DecimalField("Себестоимость", max_digits=12, decimal_places=2, default=Decimal("0.00"))
    stock = models.DecimalField("Остаток", max_digits=12, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField("Статус", max_length=16, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def get_absolute_url(self):
        return reverse("crm:product_detail", kwargs={"pk": self.pk})
