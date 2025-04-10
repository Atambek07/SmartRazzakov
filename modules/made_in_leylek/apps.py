# modules/made_in_leylek/made_in_leylek/apps.py
from django.apps import AppConfig

class MadeInLeylekConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.made_in_leylek'
    verbose_name = 'Made in Leylek Marketplace'

    def ready(self):
        # Импорт сигналов и задач при запуске приложения
        import modules.made_in_leylek.signals  # noqa
        from .tasks import start_background_tasks
        start_background_tasks()