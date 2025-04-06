"""
Presentation Layer Initialization

Экспортирует все необходимые компоненты для работы presentation слоя:
- Роутеры FastAPI
- View-классы Django REST Framework
- Сериализаторы
"""

from .views import (
    fastapi_router,
    RouteListView,
    RouteDetailView,
    TrafficAlertView,
    TrafficAnalysisView
)
from .serializers import (
    RouteInputSerializer,
    RouteOutputSerializer,
    RouteUpdateSerializer,
    TransportSerializer,
    TransportLocationSerializer,
    TransportTypeSerializer,
    TrafficAlertSerializer,
    TrafficAnalysisSerializer
)

__all__ = [
    # Роутеры
    'fastapi_router',
    
    # Views
    'RouteListView',
    'RouteDetailView',
    'TrafficAlertView',
    'TrafficAnalysisView',
    
    # Сериализаторы
    'RouteInputSerializer',
    'RouteOutputSerializer',
    'RouteUpdateSerializer',
    'TransportSerializer',
    'TransportLocationSerializer',
    'TransportTypeSerializer',
    'TrafficAlertSerializer',
    'TrafficAnalysisSerializer'
]