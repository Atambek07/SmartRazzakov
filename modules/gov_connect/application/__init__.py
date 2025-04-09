# modules/gov_connect/application/__init__.py
"""
Application Layer модуля GovConnect

Содержит всю бизнес-логику и DTO для:
- Обработки жалоб и предложений
- Управления электронной очередью
- Организации голосований
- Интеграции с внешними сервисами

Структура:
- dto: Data Transfer Objects для безопасной передачи данных между слоями
- use_cases: Реализация бизнес-сценариев
- exceptions: Кастомные исключения уровня приложения
"""

from .dto import (
    # Complaint-related DTOs
    ComplaintBaseDTO,
    ComplaintCreateDTO,
    ComplaintUpdateDTO,
    ComplaintResponseDTO,
    ComplaintStatusDTO,
    
    # Booking-related DTOs
    BookingCreateDTO,
    BookingUpdateDTO,
    BookingResponseDTO,
    SlotAvailabilityDTO,
    
    # Voting-related DTOs
    VotingCreateDTO,
    VoteCastDTO,
    VotingResultsDTO
)

from .use_cases import (
    # Complaint Processing
    ComplaintProcessingUseCase,
    ComplaintStatusUpdateUseCase,
    ComplaintModerationUseCase,
    
    # Booking Management
    BookingManagementUseCase,
    SlotAvailabilityUseCase,
    
    # Voting System
    VotingCreationUseCase,
    VoteProcessingUseCase,
    VotingResultsUseCase
)

from .exceptions import (
    GovConnectException,
    InvalidGeoDataError,
    BookingConflictError,
    VotingPermissionError,
    ComplaintModerationError
)

__all__ = [
    # DTOs
    'ComplaintBaseDTO',
    'ComplaintCreateDTO',
    'ComplaintUpdateDTO',
    'ComplaintResponseDTO',
    'ComplaintStatusDTO',
    'BookingCreateDTO',
    'BookingUpdateDTO',
    'BookingResponseDTO',
    'SlotAvailabilityDTO',
    'VotingCreateDTO',
    'VoteCastDTO',
    'VotingResultsDTO',
    
    # Use Cases
    'ComplaintProcessingUseCase',
    'ComplaintStatusUpdateUseCase',
    'ComplaintModerationUseCase',
    'BookingManagementUseCase',
    'SlotAvailabilityUseCase',
    'VotingCreationUseCase',
    'VoteProcessingUseCase',
    'VotingResultsUseCase',
    
    # Exceptions
    'GovConnectException',
    'InvalidGeoDataError',
    'BookingConflictError',
    'VotingPermissionError',
    'ComplaintModerationError'
]

# Инициализация сервисов при старте приложения
def initialize_services(config):
    """Инициализирует зависимости уровня приложения"""
    from ..infrastructure.repositories import (
        DjangoComplaintRepository,
        DjangoBookingRepository,
        RedisVotingRepository
    )
    from ..domain.services import (
        ComplaintService,
        BookingService,
        VotingService,
        GeoValidationService,
        AIModerationService
    )
    
    # Конфигурация репозиториев
    complaint_repo = DjangoComplaintRepository()
    booking_repo = DjangoBookingRepository()
    voting_repo = RedisVotingRepository(redis_uri=config.REDIS_URI)
    
    # Инициализация сервисов
    geo_service = GeoValidationService(
        gis_api_key=config.GIS_API_KEY
    )
    ai_service = AIModerationService(
        model_path=config.AI_MODERATION_MODEL
    )
    
    return {
        'complaint_service': ComplaintService(
            repo=complaint_repo,
            geo_service=geo_service
        ),
        'booking_service': BookingService(
            repo=booking_repo,
            qr_generator=config.QR_SERVICE
        ),
        'voting_service': VotingService(
            repo=voting_repo,
            auth_service=config.AUTH_PROVIDER
        ),
        'moderation_service': ai_service
    }