from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime

class TrafficSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TrafficType(str, Enum):
    ACCIDENT = "accident"
    CONSTRUCTION = "construction"
    POLICE = "police"
    WEATHER = "weather"
    EVENT = "event"

class TrafficAlertDTO(BaseModel):
    alert_id: str = Field(..., example="550e8400-e29b-41d4-a716-446655440000")
    location: tuple[float, float] = Field(..., example=(40.1234, 72.3456))
    radius_m: float = Field(..., gt=0, example=500)
    severity: TrafficSeverity
    alert_type: TrafficType
    description: str = Field(..., max_length=500)
    start_time: datetime
    end_time: Optional[datetime] = None
    affected_routes: List[str] = Field(default_factory=list)
    confirmed: bool = Field(default=False)

class TrafficAnalysisDTO(BaseModel):
    timestamp: datetime
    hotspots: List[tuple[float, float]]
    average_speed_kmh: float
    congestion_level: float = Field(..., ge=0, le=1)
    predicted_duration_min: float
    alternative_routes: List[dict]