from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = "Sayt kontenti"

    def ready(self):
        from app import signals  # noqa: F401
