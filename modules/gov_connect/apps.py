# modules/gov_connect/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class GovConnectConfig(AppConfig):
    name = 'modules.gov_connect'
    verbose_name = _("Гос. взаимодействие")

    def ready(self):
        # Инициализация сигналов и задач Celery
        from . import signals  # noqa
        from .tasks import setup_periodic_tasks  # noqa
        
        try:
            setup_periodic_tasks()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to setup periodic tasks: {str(e)}")