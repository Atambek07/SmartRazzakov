from datetime import datetime
from typing import Dict, Any
from ...domain.entities import NewsPriority, NewsArticle
from ...domain.services import NewsService, EmergencyService
from ..dto.news_dto import NewsCreateDTO
from core.utils.responses import ResponseSuccess, ResponseFailure
from modules.city_routes.domain.services import TrafficManagementService
from modules.health_connect.domain.services import EmergencyBroadcastService

class EmergencyAlertUseCase:
    def __init__(
        self,
        news_service: NewsService,
        emergency_service: EmergencyService,
        traffic_service: TrafficManagementService,
        health_service: EmergencyBroadcastService
    ):
        self.news_service = news_service
        self.emergency_service = emergency_service
        self.traffic_service = traffic_service
        self.health_service = health_service

    async def create_emergency_alert(self, alert_data: Dict[str, Any]) -> ResponseSuccess:
        try:
            # Автоматическая генерация контента
            content = await self._generate_alert_content(alert_data)
            
            emergency_article = NewsArticle(
                title=alert_data['title'],
                content=content,
                category=NewsCategory.EMERGENCY,
                priority=NewsPriority.CRITICAL,
                geo_location=alert_data.get('geo_location'),
                sources=[alert_data['source']],
                is_published=True,
                publish_at=datetime.now()
            )
            
            result = await self.news_service.create(emergency_article)
            
            # Рассылка через все доступные каналы
            await self.emergency_service.broadcast_alert(
                alert_data=alert_data,
                article_id=result.id
            )
            
            # Интеграция с городскими системами
            if 'traffic' in alert_data['tags']:
                await self.traffic_service.update_road_conditions(
                    alert_data['geo_location'],
                    "EMERGENCY"
                )
            
            if 'health' in alert_data['tags']:
                await self.health_service.activate_emergency_protocol(
                    alert_data['geo_location']
                )
            
            return ResponseSuccess(result.to_dto(NewsResponseDTO))
        
        except Exception as e:
            return ResponseFailure(str(e))

    async def _generate_alert_content(self, alert_data: Dict) -> str:
        template = await self.emergency_service.get_template(alert_data['type'])
        return template.format(
            location=alert_data.get('geo_location', 'unknown location'),
            details=alert_data.get('details', ''),
            instructions=alert_data.get('instructions', '')
        )