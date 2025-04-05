from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class ContentType(Enum):
    TEXT = "text"
    AUDIO = "audio"
    MIXED = "mixed"

@dataclass
class Story:
    id: int
    title: str
    content: dict  # {text: str, audio: Optional[str]}
    content_type: ContentType
    location: str  # GPS coordinates
    author_id: int
    created_at: datetime
    is_approved: bool = False