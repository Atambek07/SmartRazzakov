# modules/community_hub/presentation/__init__.py
"""
Presentation Layer - отвечает за взаимодействие с внешним миром через API

Содержит:
- Маршрутизацию URL
- Сериализаторы для преобразования данных
- View-классы для обработки запросов
- Потребители WebSocket
- Промежуточное ПО (middleware)
- Утилиты для работы с API
"""

from typing import Dict, Type, Any
from enum import Enum
import logging
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


class APIErrorCode(str, Enum):
    """Коды стандартных ошибок API"""
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    PERMISSION_DENIED = "permission_denied"
    INTERNAL_ERROR = "internal_error"
    BAD_REQUEST = "bad_request"


class APIError(Exception):
    """Стандартное исключение для ошибок API"""

    def __init__(
            self,
            message: str,
            code: APIErrorCode = APIErrorCode.BAD_REQUEST,
            status_code: int = status.HTTP_400_BAD_REQUEST,
            details: Dict[str, Any] = None
    ):
        self.message = message
        self.code = code
        self.status = status_code
        self.details = details or {}
        super().__init__(message)


def api_response(
        data: Any = None,
        status: int = status.HTTP_200_OK,
        metadata: Dict[str, Any] = None
) -> Response:
    """Стандартизированный формат успешного ответа API"""
    response_data = {
        "data": data,
        "meta": metadata or {}
    }
    return Response(response_data, status=status)


def error_response(
        error: APIError
) -> Response:
    """Стандартизированный формат ответа с ошибкой"""
    return Response(
        {
            "error": {
                "message": error.message,
                "code": error.code,
                "details": error.details
            }
        },
        status=error.status
    )


# Реэкспорт основных компонентов
from .serializers import (
    CommunitySerializer,
    CommunityDetailSerializer,
    CommunityCreateSerializer,
    EventSerializer,
    EventCreateSerializer,
    MemberSerializer,
    MemberRoleSerializer
)

from .views import (
    CommunityViewSet,
    EventViewSet,
    ModerationViewSet
)

from .consumers import (
    ChatConsumer
)

from .routing import websocket_urlpatterns

__all__ = [
    # Основные классы
    'APIError',
    'APIErrorCode',

    # Вспомогательные функции
    'api_response',
    'error_response',

    # Сериализаторы
    'CommunitySerializer',
    'CommunityDetailSerializer',
    'CommunityCreateSerializer',
    'EventSerializer',
    'EventCreateSerializer',
    'MemberSerializer',
    'MemberRoleSerializer',

    # View
    'CommunityViewSet',
    'EventViewSet',
    'ModerationViewSet',

    # WebSocket
    'ChatConsumer',
    'websocket_urlpatterns'
]


def setup_presentation_layer():
    """Инициализация presentation слоя"""
    logger.info("Initializing CommunityHub presentation layer")

    # Здесь может быть дополнительная настройка
    # например, регистрация кастомных обработчиков ошибок

    return {
        'version': '1.0',
        'routes_registered': True
    }