from django.apps import AppConfig


class CityRoutesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.city_routes'

    def ready(self):
        from .tasks import update_vehicle_locations
        from .signals import process_traffic_data
