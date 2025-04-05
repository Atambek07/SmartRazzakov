from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

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
    stops: List[str]  # List of stop IDs
    schedule: dict    # { "weekdays": [...], "weekends": [...] }
    current_location: Optional[str] = None  # GPS coordinates