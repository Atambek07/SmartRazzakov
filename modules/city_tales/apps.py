from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CityTalesConfig(AppConfig):
    """Конфигурация приложения CityTales"""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'city_tales'
    verbose_name = _('Городские истории')

    def ready(self):
        # Импорт сигналов и задач
        try:
            from . import signals  # noqa
            from .tasks import update_qr_codes  # noqa
            
            # Инициализация периодических задач
            self._init_scheduler()
        except ImportError:
            pass

    def _init_scheduler(self):
        """Инициализация планировщика задач"""
        from django_q.tasks import schedule
        from django_q.models import Schedule

        if not Schedule.objects.filter(func='city_tales.tasks.update_qr_codes').exists():
            schedule(
                'city_tales.tasks.update_qr_codes',
                schedule_type=Schedule.DAILY,
                name='Daily QR Codes Update'
            )