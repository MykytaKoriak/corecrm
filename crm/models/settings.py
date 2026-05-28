from django.db import models


class CustomField(models.Model):
    class FieldType(models.TextChoices):
        TEXT = "text", "Текст"
        NUMBER = "number", "Число"
        DATE = "date", "Дата"
        BOOLEAN = "boolean", "Да/нет"

    entity = models.CharField("Сущность", max_length=64)
    name = models.CharField("Название", max_length=120)
    field_type = models.CharField("Тип", max_length=16, choices=FieldType.choices, default=FieldType.TEXT)
    is_required = models.BooleanField("Обязательное", default=False)
    is_active = models.BooleanField("Активно", default=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Пользовательское поле"
        verbose_name_plural = "Пользовательские поля"
        ordering = ["entity", "name"]

    def __str__(self):
        return f"{self.entity}: {self.name}"
