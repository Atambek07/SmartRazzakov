from datetime import datetime, timedelta
from city_routes.domain.entities import TrafficAlert
from city_routes.application.dto.traffic_dto import TrafficAlertDTO, TrafficAnalysisDTO


class TrafficManagementUseCase:
    def __init__(self, traffic_repository, integration_service):
        self.repository = traffic_repository
        self.integration = integration_service

    async def create_alert(self, alert_data: TrafficAlertDTO) -> TrafficAlert:
        alert = TrafficAlert(
            location=alert_data.location,
            radius=alert_data.radius_m,
            severity=alert_data.severity,
            alert_type=alert_data.alert_type,
            description=alert_data.description,
            start_time=alert_data.start_time,
            end_time=alert_data.end_time or datetime.now() + timedelta(hours=2)
        )
        return await self.repository.save(alert)

    async def analyze_traffic(self) -> TrafficAnalysisDTO:
        live_data = await self.integration.get_live_traffic()
        prediction = await self.integration.predict_congestion()

        return TrafficAnalysisDTO(
            timestamp=datetime.now(),
            hotspots=live_data.hotspots,
            average_speed_kmh=live_data.avg_speed,
            congestion_level=prediction.congestion_level,
            predicted_duration_min=prediction.estimated_delay,
            alternative_routes=prediction.alternatives
        )