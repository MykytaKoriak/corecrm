from django.conf import settings
from django.db import models
from django.urls import reverse


class Client(models.Model):
    class ClientType(models.TextChoices):
        PERSON = "person", "Физическое лицо"
        COMPANY = "company", "Компания"

    class Status(models.TextChoices):
        NEW = "new", "Новый"
        ACTIVE = "active", "Активный"
        VIP = "vip", "VIP"
        ARCHIVED = "archived", "Архив"

    name = models.CharField("Имя / компания", max_length=255, blank=True)
    client_type = models.CharField("Тип", max_length=16, choices=ClientType.choices, default=ClientType.PERSON)
    status = models.CharField("Статус", max_length=16, choices=Status.choices, default=Status.NEW)
    phone = models.CharField("Основной телефон", max_length=40, blank=True)
    extra_phones = models.JSONField("Дополнительные телефоны", default=list, blank=True)
    email = models.EmailField("Основной email", blank=True)
    extra_emails = models.JSONField("Дополнительные email", default=list, blank=True)
    telegram = models.CharField("Telegram", max_length=120, blank=True)
    instagram = models.CharField("Instagram", max_length=255, blank=True)
    company_name = models.CharField("Компания", max_length=255, blank=True)
    primary_contact_name = models.CharField("Имя обратившегося", max_length=160, blank=True)
    delivery_address = models.TextField("Адрес доставки", blank=True)
    legal_address = models.TextField("Юридический адрес", blank=True)
    tags = models.JSONField("Теги", default=list, blank=True)
    notes = models.TextField("Внутренние заметки", blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Ответственный", null=True, blank=True, on_delete=models.SET_NULL, related_name="crm_clients")
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["-updated_at", "-created_at"]

    def __str__(self):
        return self.company_name or self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.company_name or self.primary_contact_name
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("crm:client_detail", kwargs={"pk": self.pk})


class ContactPerson(models.Model):
    client = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField("Имя", max_length=160)
    position = models.CharField("Должность", max_length=120, blank=True)
    phone = models.CharField("Телефон", max_length=40, blank=True)
    email = models.EmailField("Email", blank=True)
    telegram = models.CharField("Telegram", max_length=120, blank=True)
    is_primary = models.BooleanField("Основной контакт", default=False)

    class Meta:
        verbose_name = "Контактное лицо"
        verbose_name_plural = "Контактные лица"
        ordering = ["-is_primary", "name"]

    def __str__(self):
        return f"{self.name} · {self.client}"


class ClientFile(models.Model):
    client = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.CASCADE, related_name="files")
    file = models.FileField("Файл", upload_to="clients/%Y/%m/")
    title = models.CharField("Название", max_length=180, blank=True)
    comment = models.CharField("Комментарий", max_length=255, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Загрузил", null=True, blank=True, on_delete=models.SET_NULL)
    uploaded_at = models.DateTimeField("Загружен", auto_now_add=True)

    class Meta:
        verbose_name = "Файл клиента"
        verbose_name_plural = "Файлы клиентов"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title or self.file.name
