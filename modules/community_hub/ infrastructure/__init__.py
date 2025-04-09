# modules/community_hub/infrastructure/__init__.py
"""
Инициализация инфраструктурного слоя CommunityHub

Содержит:
- Репозитории для работы с данными
- Интеграции с внешними сервисами
- Адаптеры для баз данных и других инфраструктурных компонентов
"""

from typing import Type, Dict, Any, Optional
from dataclasses import dataclass
import logging
from uuid import UUID

# Настройка логгера
logger = logging.getLogger(__name__)


@dataclass
class DatabaseConfig:
    """Конфигурация подключения к базе данных"""
    host: str
    port: int
    user: str
    password: str
    name: str
    engine: str = "postgresql"
    pool_size: int = 20
    timeout: int = 30


@dataclass
class CacheConfig:
    """Конфигурация кеширования"""
    host: str
    port: int
    db: int = 0
    password: Optional[str] = None
    timeout: int = 5
    default_ttl: int = 3600  # 1 час


class InfrastructureError(Exception):
    """Базовое исключение для инфраструктурных ошибок"""

    def __init__(self, component: str, message: str):
        self.component = component
        self.message = message
        super().__init__(f"{component} error: {message}")


# Реэкспорт основных компонентов
from .repositories import (
    CommunityRepository,
    EventRepository,
    MemberRepository,
    PostRepository
)

from .integrations import (
    EmailServiceClient,
    SMSServiceClient,
    PaymentServiceClient,
    StorageServiceClient,
    RealtimeNotificationService,
    CommunityWebSocketClient
)

from .models import (
    CommunityModel,
    CommunityMemberModel,
    CommunityEventModel,
    CommunityPostModel
)

__all__ = [
    # Конфигурация
    'DatabaseConfig',
    'CacheConfig',

    # Репозитории
    'CommunityRepository',
    'EventRepository',
    'MemberRepository',
    'PostRepository',

    # Интеграции
    'EmailServiceClient',
    'SMSServiceClient',
    'PaymentServiceClient',
    'StorageServiceClient',
    'RealtimeNotificationService',
    'CommunityWebSocketClient',

    # Модели
    'CommunityModel',
    'CommunityMemberModel',
    'CommunityEventModel',
    'CommunityPostModel',

    # Исключения
    'InfrastructureError'
]


def init_infrastructure(
        db_config: DatabaseConfig,
        cache_config: CacheConfig,
        enable_cache: bool = True
) -> Dict[str, Any]:
    """
    Инициализация инфраструктурных компонентов

    Args:
        db_config: Конфигурация базы данных
        cache_config: Конфигурация кеширования
        enable_cache: Включить ли кеширование

    Returns:
        Словарь с инициализированными компонентами:
        - repositories: Репозитории для работы с данными
        - services: Клиенты внешних сервисов
        - cache: Клиент кеша (если включен)
    """
    logger.info("Initializing CommunityHub infrastructure layer")

    components = {
        'repositories': {
            'community': CommunityRepository(),
            'event': EventRepository(),
            'member': MemberRepository(),
            'post': PostRepository()
        },
        'services': {
            'email': EmailServiceClient(),
            'sms': SMSServiceClient(),
            'payment': PaymentServiceClient(),
            'storage': StorageServiceClient(),
            'realtime': RealtimeNotificationService(),
            'websocket': CommunityWebSocketClient()
        }
    }

    if enable_cache:
        try:
            # Инициализация Redis клиента
            from redis import asyncio as aioredis
            components['cache'] = aioredis.Redis(
                host=cache_config.host,
                port=cache_config.port,
                db=cache_config.db,
                password=cache_config.password,
                socket_timeout=cache_config.timeout
            )
            logger.info("Cache layer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize cache: {str(e)}")
            raise InfrastructureError("Cache", str(e))

    logger.info("Infrastructure layer initialized")
    return components