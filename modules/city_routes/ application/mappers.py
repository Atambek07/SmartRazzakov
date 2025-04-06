from datetime import datetime
from typing import Optional
from city_routes.domain.entities import Route, TrafficAlert
from city_routes.application.dto import (
    RouteResponseDTO,
    RouteRequestDTO,
    TrafficAlertDTO
)

def route_to_dto(route: Route) -> RouteResponseDTO:
    """Конвертирует доменную сущность Route в DTO для ответа"""
    return RouteResponseDTO(
        route_id=str(route.id),
        distance_km=route.distance_km,
        duration_min=route.estimated_duration_min,
        polyline=route.waypoints,
        transport_type=route.transport_type,
        created_at=route.created_at or datetime.now(),
        eco_score=_calculate_eco_score(route),
        accessibility_features=_get_accessibility_features(route)
    )

def dto_to_route(dto: RouteRequestDTO) -> Route:
    """Конвертирует DTO запроса в доменную сущность Route"""
    return Route(
        start_point=(dto.start_lat, dto.start_lon),
        end_point=(dto.end_lat, dto.end_lon),
        waypoints=[],
        distance_km=0.0,  # Будет рассчитано при построении маршрута
        transport_type=dto.transport,
        wheelchair_accessible=dto.wheelchair_accessible,
        avoid_tolls=dto.avoid_tolls
    )

def alert_to_dto(alert: TrafficAlert) -> TrafficAlertDTO:
    """Конвертирует доменную сущность TrafficAlert в DTO"""
    return TrafficAlertDTO(
        alert_id=str(alert.id),
        location=alert.location,
        radius_m=alert.radius,
        severity=alert.severity,
        alert_type=alert.alert_type,
        description=alert.description,
        start_time=alert.start_time,
        end_time=alert.end_time,
        affected_routes=[str(r) for r in alert.affected_routes],
        confirmed=alert.is_confirmed
    )

def dto_to_alert(dto: TrafficAlertDTO) -> TrafficAlert:
    """Конвертирует DTO в доменную сущность TrafficAlert"""
    return TrafficAlert(
        location=dto.location,
        radius=dto.radius_m,
        severity=dto.severity,
        alert_type=dto.alert_type,
        description=dto.description,
        start_time=dto.start_time,
        end_time=dto.end_time
    )

# Вспомогательные приватные функции
def _calculate_eco_score(route: Route) -> float:
    """Рассчитывает экологическую оценку маршрута"""
    eco_factors = {
        'bus': 0.8,
        'metro': 0.9,
        'bike': 1.0,
        'pedestrian': 1.0,
        'taxi': 0.4
    }
    base_score = eco_factors.get(route.transport_type, 0.5)
    return base_score * 10  # Приводим к шкале 0-10

def _get_accessibility_features(route: Route) -> list[str]:
    """Определяет особенности доступности маршрута"""
    features = []
    if getattr(route, 'wheelchair_accessible', False):
        features.append("wheelchair")
    if getattr(route, 'has_elevator', False):
        features.append("elevator")
    if getattr(route, 'has_audio_guidance', False):
        features.append("audio_guidance")
    return features