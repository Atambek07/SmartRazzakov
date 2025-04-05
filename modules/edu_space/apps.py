from django.apps import AppConfig


class EduSpaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.edu_space'

    def ready(self):
        # Импорт сигналов и задач Celery
        from . import signals
        from .tasks import schedule_reminders