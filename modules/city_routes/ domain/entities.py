from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Tuple, Optional

class TransportType(str, Enum):
    BUS = "bus"
    METRO = "metro"
    BIKE = "bike"
    PEDESTRIAN = "pedestrian"
    TAXI = "taxi"

class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Route:
    id: str
    start_point: Tuple[float, float]  # (latitude, longitude)
    end_point: Tuple[float, float]
    waypoints: List[Tuple[float, float]]
    distance_km: float
    estimated_duration_min: float
    transport_type: TransportType
    created_at: datetime = datetime.now()
    wheelchair_accessible: bool = False
    avoid_tolls: bool = False
    eco_score: Optional[float] = None

    def calculate_eco_friendliness(self) -> float:
        """Calculate eco-score based on transport type and distance"""
        eco_factors = {
            TransportType.BUS: 0.8,
            TransportType.METRO: 0.9,
            TransportType.BIKE: 1.0,
            TransportType.PEDESTRIAN: 1.0,
            TransportType.TAXI: 0.4
        }
        return eco_factors.get(self.transport_type, 0.5) * 10

@dataclass
class TrafficAlert:
    id: str
    location: Tuple[float, float]
    radius_m: float
    severity: AlertSeverity
    alert_type: str  # "accident", "construction", etc.
    description: str
    start_time: datetime
    end_time: Optional[datetime] = None
    is_active: bool = True
    affected_routes: List[str] = None  # List of route IDs

    def __post_init__(self):
        if self.affected_routes is None:
            self.affected_routes = []

@dataclass
class TransportVehicle:
    id: str
    vehicle_type: TransportType
    current_location: Tuple[float, float]
    capacity: int
    available: bool = True
    last_maintenance: Optional[datetime] = None

@dataclass
class UserPreferences:
    user_id: str
    preferred_transport: List[TransportType]
    avoid_stairs: bool = False
    max_walking_distance_m: int = 500
    notification_preferences: dict = None

    def __post_init__(self):
        if self.notification_preferences is None:
            self.notification_preferences = {
                'route_updates': True,
                'traffic_alerts': True,
                'promotions': False
            }