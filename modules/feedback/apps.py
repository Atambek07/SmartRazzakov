# modules/feedback/apps.py
from django.apps import AppConfig

class FeedbackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.feedback'
    verbose_name = 'Управление отзывами'

    def ready(self):
        from . import signals  # noqa
        from .tasks import start_periodic_tasks  # noqa
        start_periodic_tasks()