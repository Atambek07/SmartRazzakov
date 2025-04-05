from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List

class NewsCategory(Enum):
    POLITICS = "politics"
    ECONOMY = "economy"
    CULTURE = "culture"
    EMERGENCY = "emergency"
    TRANSPORT = "transport"

class NewsPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class NewsItem:
    id: str
    title: str
    content: str
    category: NewsCategory
    priority: NewsPriority
    publish_date: datetime
    source: str
    is_verified: bool = False
    location: Optional[str] = None  # GPS coordinates
    related_links: Optional[List[str]] = None
    image_url: Optional[str] = None