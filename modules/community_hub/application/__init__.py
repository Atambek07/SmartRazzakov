# modules/community_hub/application/__init__.py
from typing import List, Type, Dict
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import logging

# Настройка логгера
logger = logging.getLogger(__name__)


# ====================== Базовые типы и исключения ======================
class AppErrorType(str, Enum):
    """Типы ошибок приложения"""
    VALIDATION = "validation_error"
    AUTH = "authentication_error"
    NOT_FOUND = "not_found_error"
    INTEGRATION = "integration_error"
    BUSINESS = "business_rule_error"


@dataclass
class AppError:
    """Стандартная ошибка приложения"""
    error_type: AppErrorType
    message: str
    details: Dict = None
    code: str = None


class CommunityHubException(Exception):
    """Базовое исключение для модуля"""

    def __init__(self, error: AppError):
        self.error = error
        super().__init__(error.message)


# ====================== DTO реэкспорт ======================
from .dto import (
    # Community DTOs
    CommunityCreateDTO,
    CommunityUpdateDTO,
    CommunityResponseDTO,
    CommunityListDTO,
    CommunityStatsDTO,
    CommunitySearchDTO,

    # Event DTOs
    EventCreateDTO,
    EventUpdateDTO,
    EventResponseDTO,
    EventListDTO,

    # Member DTOs
    MemberDTO,
    MemberUpdateDTO,
    MemberListDTO,

    # Post DTOs
    PostCreateDTO,
    PostResponseDTO,

    # Chat DTOs
    MessageDTO,
    ChatChannelDTO,

    # System DTOs
    BadgeDTO,
    ReportDTO,
    AnalyticsDTO,

    # Response DTOs
    SuccessResponse,
    ErrorResponse,
    PaginatedResponse
)

# ====================== Use Cases реэкспорт ======================
from .use_cases import (
    # Community Management
    CreateCommunityUseCase,
    UpdateCommunityUseCase,
    DeleteCommunityUseCase,
    SearchCommunitiesUseCase,
    GetCommunityDetailsUseCase,

    # Event Management
    CreateEventUseCase,
    UpdateEventUseCase,
    CancelEventUseCase,
    GetEventDetailsUseCase,
    ListCommunityEventsUseCase,

    # Member Management
    JoinCommunityUseCase,
    LeaveCommunityUseCase,
    UpdateMemberRoleUseCase,
    ListCommunityMembersUseCase,

    # Content Moderation
    CreatePostUseCase,
    UpdatePostUseCase,
    DeletePostUseCase,
    ModeratePostUseCase,
    CreateReportUseCase,
    HandleReportUseCase,

    # Notification System
    SendNotificationUseCase,
    MarkNotificationReadUseCase
)


# ====================== Сервисы ======================
class NotificationService:
    """Абстракция для сервиса нотификаций"""

    async def send(self, user_id: str, message: str, data: dict = None):
        raise NotImplementedError


class AnalyticsService:
    """Сервис аналитики сообщества"""

    async def track_event(self, event_type: str, metadata: dict = None):
        raise NotImplementedError


# ====================== Конфигурация ======================
@dataclass
class CommunityHubConfig:
    """Конфигурация модуля CommunityHub"""
    max_communities_per_user: int = 10
    max_members_per_community: int = 5000
    default_page_size: int = 20
    max_tags_per_community: int = 15
    event_reminder_hours: int = 24
    report_expiry_days: int = 30


# ====================== Модели ответов ======================
@dataclass
class CommunityOperationResult:
    """Результат операции с сообществом"""
    success: bool
    community: CommunityResponseDTO
    timestamp: datetime = datetime.utcnow()
    warnings: List[str] = None


@dataclass
class EventOperationResult:
    """Результат операции с событием"""
    success: bool
    event: EventResponseDTO
    affected_members: int
    timestamp: datetime = datetime.utcnow()


# ====================== Вспомогательные функции ======================
def setup_application(config: CommunityHubConfig = None):
    """Инициализация application слоя"""
    logger.info("Initializing CommunityHub application layer")

    # Создаем дефолтную конфигурацию если не передана
    app_config = config or CommunityHubConfig()

    # Здесь может быть инициализация сервисов, репозиториев и т.д.
    logger.info(f"CommunityHub configured with: {app_config}")

    return {
        'config': app_config,
        'services': {
            'notification': NotificationService(),
            'analytics': AnalyticsService()
        }
    }


# Реэкспорт основных компонентов
__all__ = [
    # DTO
    'CommunityCreateDTO', 'CommunityUpdateDTO', 'CommunityResponseDTO',
    'EventCreateDTO', 'EventResponseDTO',
    'MemberDTO', 'PostCreateDTO',

    # Use Cases
    'CreateCommunityUseCase', 'UpdateCommunityUseCase',
    'CreateEventUseCase', 'CancelEventUseCase',
    'ModeratePostUseCase',

    # Исключения
    'CommunityHubException', 'AppError',

    # Сервисы
    'NotificationService', 'AnalyticsService',

    # Вспомогательное
    'setup_application'
]