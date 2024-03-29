from django.apps import AppConfig


class HireUsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hire_us"

    def ready(self) -> None:
        import hire_us.signals
