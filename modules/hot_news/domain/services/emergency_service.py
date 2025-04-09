from abc import ABC, abstractmethod
from typing import Dict, Any
from ...domain.entities import NewsArticle
from modules.health_connect.domain.services import EmergencyProtocolService
from modules.city_routes.domain.services import TrafficUpdateService

class EmergencyService(ABC):
    @abstractmethod
    async def broadcast_alert(
        self,
        alert_data: Dict[str, Any],
        article_id: str
    ) -> int:
        """Рассылает экстренное уведомление через все каналы"""
        pass

    @abstractmethod
    async def verify_emergency_source(self, source_id: str) -> bool:
        pass

    @abstractmethod
    async def get_emergency_template(self, alert_type: str) -> str:
        pass

    @abstractmethod
    async def activate_city_protocols(
        self,
        alert_data: Dict[str, Any],
        health_service: EmergencyProtocolService,
        traffic_service: TrafficUpdateService
    ) -> None:
        pass