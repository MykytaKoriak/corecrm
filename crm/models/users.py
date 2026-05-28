from django.conf import settings
from django.db import models


class Profile(models.Model):
    class Role(models.TextChoices):
        ADMIN = "admin", "Администратор"
        DIRECTOR = "director", "Руководитель"
        MANAGER = "manager", "Менеджер"
        PRODUCTION = "production", "Склад / производство"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="profile")
    role = models.CharField("Роль", max_length=32, choices=Role.choices, default=Role.MANAGER)
    phone = models.CharField("Телефон", max_length=32, blank=True)
    position = models.CharField("Должность", max_length=120, blank=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} · {self.get_role_display()}"
