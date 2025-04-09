# Импорт основных компонентов presentation слоя
from .serializers import (
    EducationalContentSerializer,
    CourseSerializer,
    UserProfileSerializer,
    PublicUserSerializer,
    LiveSessionSerializer,
    InteractiveTestSerializer,
    TutorAvailabilitySerializer
)

from .views import (
    CourseViewSet,
    ContentViewSet,
    TutorViewSet
)

from .schemas import (
    CourseViewSetSchema,
    ContentViewSetSchema,
    TutorViewSetSchema
)

from .urls import urlpatterns as presentation_urls

__all__ = [
    # Сериализаторы
    'EducationalContentSerializer',
    'CourseSerializer',
    'UserProfileSerializer',
    'PublicUserSerializer',
    'LiveSessionSerializer',
    'InteractiveTestSerializer',
    'TutorAvailabilitySerializer',
    
    # Представления
    'CourseViewSet',
    'ContentViewSet',
    'TutorViewSet',
    
    # Схемы документации
    'CourseViewSetSchema',
    'ContentViewSetSchema',
    'TutorViewSetSchema',
    
    # URL-маршруты
    'presentation_urls'
]

# Инициализация логирования
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Автоматическое подключение сигналов
try:
    from .signals import register_signals
    register_signals()
except ImportError as e:
    logger.warning(f"Signals not registered: {str(e)}")