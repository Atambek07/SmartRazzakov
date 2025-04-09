from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class HotNewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.hot_news'
    verbose_name = _('Горячие новости и подписки')

    def ready(self):
        # Импорт сигналов и обработчиков
        try:
            from .infrastructure import signals  # noqa F401
        except ImportError:
            pass