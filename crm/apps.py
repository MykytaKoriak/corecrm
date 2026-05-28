from django.apps import AppConfig


class CrmConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "crm"
    verbose_name = "CRM"

    def ready(self):
        import crm.services.activity  # noqa: F401
        import crm.services.notifications  # noqa: F401
