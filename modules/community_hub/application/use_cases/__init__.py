# modules/community_hub/application/use_cases/__init__.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional
from ...domain.entities import Community, CommunityEvent, CommunityMember
from ...domain.exceptions import (
    CommunityNotFoundException,
    PermissionDeniedException,
    ValidationException
)

T = TypeVar('T')

class BaseUseCase(ABC):
    @abstractmethod
    async def execute(self, *args, **kwargs) -> T:
        raise NotImplementedError

class CommunityBaseUseCase(BaseUseCase, Generic[T]):
    def _validate_community_exists(self, community: Optional[Community]):
        if not community:
            raise CommunityNotFoundException()

# Реэкспорт всех use cases
from .community_management import (
    CreateCommunityUseCase,
    UpdateCommunityUseCase,
    SearchCommunitiesUseCase
)
from .event_management import (
    CreateEventUseCase,
    CancelEventUseCase,
    GetCommunityEventsUseCase
)
from .content_moderation import (
    ModeratePostUseCase,
    CreateReportUseCase,
    HandleUserReportUseCase
)

__all__ = [
    'CreateCommunityUseCase',
    'UpdateCommunityUseCase',
    'SearchCommunitiesUseCase',
    'CreateEventUseCase',
    'CancelEventUseCase',
    'ModeratePostUseCase',
    'CreateReportUseCase'
]