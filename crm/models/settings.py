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


class DocumentTemplate(models.Model):
    class TemplateType(models.TextChoices):
        OFFER = "offer", "Коммерческое предложение"
        INVOICE = "invoice", "Счет"
        CONTRACT = "contract", "Договор"

    name = models.CharField("Название", max_length=180)
    template_type = models.CharField("Тип", max_length=32, choices=TemplateType.choices, default=TemplateType.OFFER)
    body = models.TextField("Шаблон")
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Шаблон документа"
        verbose_name_plural = "Шаблоны документов"
        ordering = ["template_type", "name"]

    def __str__(self):
        return self.name
