# infrastructure/__init__.py

# Импорт интеграций
from .integrations import (
    MapboxProvider,
    GoogleMapsProvider,
    OSMAdapter,
    TwilioSMSService,
    KazInfoSMSService,
    YandexTrackerAdapter,
    GPSGateTracker
)

# Импорт моделей
from .models import (
    Location,
    RouteModel,
    RoutePoint,
    TransportVehicleModel,
    TransportTypeModel
)

# Импорт репозиториев
from .repositories import (
    RouteRepository,
    DjangoRouteRepository,
    TransportRepository,
    DjangoTransportRepository
)

# Экспорт всех компонентов
__all__ = [
    # Интеграции
    'MapboxProvider',
    'GoogleMapsProvider',
    'OSMAdapter',
    'TwilioSMSService',
    'KazInfoSMSService',
    'YandexTrackerAdapter',
    'GPSGateTracker',
    
    # Модели
    'Location',
    'RouteModel',
    'RoutePoint',
    'TransportVehicleModel',
    'TransportTypeModel',
    
    # Репозитории
    'RouteRepository',
    'DjangoRouteRepository',
    'TransportRepository',
    'DjangoTransportRepository'
]

# Конфигурация по умолчанию
DEFAULT_PROVIDERS = {
    'map': OSMAdapter,  # По умолчанию используем OSM
    'sms': KazInfoSMSService,  # Казахстанский провайдер
    'tracking': YandexTrackerAdapter
}

def get_default_provider(provider_type: str, **kwargs):
    """
    Фабрика для получения провайдера по умолчанию
    :param provider_type: 'map', 'sms' или 'tracking'
    :param kwargs: параметры для инициализации провайдера
    :return: экземпляр провайдера
    """
    provider_class = DEFAULT_PROVIDERS.get(provider_type)
    if not provider_class:
        raise ValueError(f"Unknown provider type: {provider_type}")
    return provider_class(**kwargs)