from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class TransportType(Enum):
    BUS = "bus"
    TRAM = "tram"
    TROLLEY = "trolley"
    MINIBUS = "minibus"

class RouteOptimization(Enum):
    FASTEST = "fastest"
    CHEAPEST = "cheapest"
    ECO = "eco"

@dataclass
class TransportRoute:
    id: str
    transport_type: TransportType
    number: str
    stops: list[str]  # Список ID остановок
    schedule: dict  # {"weekdays": [...], "weekends": [...]}
    current_location: tuple[float, float] | None = None  # (lat, lng)