from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class ComplaintStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    REJECTED = "rejected"

class ComplaintPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class CitizenComplaint:
    id: str
    title: str
    description: str
    location: str  # GPS coordinates
    photo_url: str
    status: ComplaintStatus
    priority: ComplaintPriority
    citizen_id: str
    created_at: datetime
    assigned_department: str = None