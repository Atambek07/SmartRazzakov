# modules/health_connect/apps.py
from django.apps import AppConfig

class HealthConnectConfig(AppConfig):
    name = 'modules.health_connect'
    verbose_name = 'Цифровое Здоровье'
    
    def ready(self):
        # Импорт обработчиков сигналов и задач Celery
        from . import signals  # noqa
        from .tasks import setup_periodic_tasks  # noqa
        
        # Инициализация фоновых задач
        if not hasattr(self, '_already_loaded'):
            from celery.schedules import crontab
            from core.celery import app as celery_app
            
            celery_app.add_periodic_task(
                crontab(hour=3, minute=30),
                self.clear_expired_sessions.s(),
                name='clear_expired_telemedicine_sessions'
            )
            self._already_loaded = True

    @staticmethod
    @celery_app.task
    def clear_expired_sessions():
        from .models import TelemedicineSession
        TelemedicineSession.objects.filter(
            status='completed'
        ).delete()