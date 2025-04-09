# modules/community_hub/infrastructure/integrations/realtime/__init__.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
from uuid import UUID

logger = logging.getLogger(__name__)

class RealtimeConnectionError(Exception):
    """Ошибка подключения к realtime-сервису"""
    pass

class BaseRealtimeClient(ABC):
    @abstractmethod
    async def connect(self):
        """Установить соединение"""
        pass

    @abstractmethod
    async def disconnect(self):
        """Закрыть соединение"""
        pass

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """Статус подключения"""
        pass

__all__ = ['BaseRealtimeClient', 'RealtimeConnectionError']