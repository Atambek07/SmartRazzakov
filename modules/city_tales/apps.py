from django.apps import AppConfig


class CityTalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.city_tales'

    def ready(self, signals=None):
        from . import signals  # Импорт сигналов