from django.apps import AppConfig


class GovConnectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.gov_connect'

    def ready(self):
        from . import signals  # Импорт сигналов
        from .tasks import process_pending_complaints