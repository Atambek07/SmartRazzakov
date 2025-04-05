from django.apps import AppConfig


class EduSpaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.edu_space'

    def ready(self):
        # Импорт сигналов и задач Celery
        from . import signals
        from .tasks import schedule_reminders


class CityTalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.city_tales'

    def ready(self):
        from . import signals  # Импорт сигналов


class CityRoutesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.city_routes'

    def ready(self):
        from .tasks import update_vehicle_locations
        from .signals import process_traffic_data


class GovConnectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.gov_connect'

    def ready(self):
        from . import signals  # Импорт сигналов
        from .tasks import process_pending_complaints