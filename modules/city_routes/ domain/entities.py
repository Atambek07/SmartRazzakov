from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Route:
    """Маршрут между двумя точками с промежуточными точками"""
    id: str
    start_point: str  # Формат: "latitude,longitude"
    end_point: str
    waypoints: List[str]  # Список координат промежуточных точек
    distance_km: float
    duration_min: int
    created_at: datetime
    is_active: bool = True

@dataclass
class TrafficInfo:
    """Данные о трафике на участке маршрута"""
    route_id: str
    congestion_level: str  # "low", "medium", "high"
    updated_at: datetime
    speed_kmh: float

@dataclass
class Transport:
    """Транспортное средство (автобус, маршрутка)"""
    id: str
    vehicle_type: str  # "bus", "minibus", "tram"
    current_location: str  # Координаты
    route_id: str  # Привязан к маршруту
    last_update: datetime