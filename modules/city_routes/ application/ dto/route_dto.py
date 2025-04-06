from pydantic import BaseModel, Field, validator # type: ignore
from typing import List, Optional
from enum import Enum
from datetime import datetime

class TransportType(str, Enum):
    BUS = "bus"
    METRO = "metro"
    BIKE = "bike"
    PEDESTRIAN = "pedestrian"
    TAXI = "taxi"

class RouteRequestDTO(BaseModel):
    start_lat: float = Field(..., ge=-90, le=90, example=40.1234, description="Широта начальной точки")
    start_lon: float = Field(..., ge=-180, le=180, example=72.3456, description="Долгота начальной точки")
    end_lat: float = Field(..., ge=-90, le=90, example=40.1256, description="Широта конечной точки")
    end_lon: float = Field(..., ge=-180, le=180, example=72.3478, description="Долгота конечной точки")
    transport: TransportType = Field(default=TransportType.BUS, description="Предпочитаемый тип транспорта")
    avoid_tolls: bool = Field(default=False, description="Избегать платных дорог")
    wheelchair_accessible: bool = Field(default=False, description="Доступ для инвалидных колясок")

    @validator('start_lat', 'end_lat')
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError("Широта должна быть между -90 и 90")
        return v

    @validator('start_lon', 'end_lon')
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError("Долгота должна быть между -180 и 180")
        return v

class RouteResponseDTO(BaseModel):
    route_id: str = Field(..., example="550e8400-e29b-41d4-a716-446655440000")
    distance_km: float = Field(..., gt=0, example=5.3)
    duration_min: float = Field(..., gt=0, example=15.5)
    polyline: List[tuple[float, float]] = Field(..., description="Список координат маршрута")
    transport_type: TransportType
    created_at: datetime
    eco_score: float = Field(..., ge=0, le=10, description="Экологичность маршрута (0-10)")
    accessibility_features: List[str] = Field(default_factory=list, description=["wheelchair", "elevator"])

class RouteUpdateDTO(BaseModel):
    route_id: str
    new_transport: Optional[TransportType] = None
    avoid_areas: Optional[List[tuple[float, float]]] = None
    priority: Optional[str] = Field(None, regex='^(fastest|shortest|eco)$')