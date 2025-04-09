# modules/community_hub/infrastructure/repositories/__init__.py
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID
from django.core.paginator import Paginator
from ...models import (
    CommunityModel,
    CommunityMemberModel,
    CommunityEventModel,
    CommunityPostModel
)

__all__ = [
    'CommunityRepository',
    'EventRepository',
    'MemberRepository',
    'PostRepository'
]


class BaseRepository(ABC):
    """Абстрактный базовый репозиторий"""

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Any:
        pass

    @abstractmethod
    async def save(self, entity: Any) -> Any:
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        pass