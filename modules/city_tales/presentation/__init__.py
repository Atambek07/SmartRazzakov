from .serializers import (
    TaleContentSerializer,
    QRRequestSerializer,
    UserPreferenceSerializer
)
from .views import TaleContentView, UserPreferenceView
from .urls import urlpatterns

__all__ = [
    'TaleContentSerializer',
    'QRRequestSerializer',
    'UserPreferenceSerializer',
    'TaleContentView',
    'UserPreferenceView',
    'urlpatterns'
]