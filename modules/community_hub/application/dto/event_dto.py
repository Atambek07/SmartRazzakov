# modules/community_hub/application/dto/event_dto.py
from datetime import datetime
from pydantic import validator, root_validator
from typing import Optional, List
from . import BaseCommunityDTO

class EventCreateDTO(BaseCommunityDTO):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=20, max_length=10000)
    start_time: datetime
    end_time: datetime
    location: str = Field(..., max_length=200)
    max_participants: Optional[int] = Field(None, gt=0)
    is_online: bool = False
    cover_image: Optional[HttpUrl] = None
    tags: List[str] = Field(default_factory=list)
    registration_required: bool = True
    recurring_settings: Optional[dict] = None

    @root_validator
    def validate_time_range(cls, values):
        start = values.get('start_time')
        end = values.get('end_time')
        if start and end and end <= start:
            raise ValueError('End time must be after start time')
        return values

class EventUpdateDTO(BaseCommunityDTO):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=20, max_length=10000)
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    location: Optional[str] = Field(None, max_length=200)
    max_participants: Optional[int] = Field(None, gt=0)
    is_online: Optional[bool] = None
    cover_image: Optional[HttpUrl] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = Field(None, regex="^(planned|ongoing|cancelled|completed)$")

class EventResponseDTO(BaseCommunityDTO):
    id: UUID
    community_id: UUID
    title: str
    description: str
    organizer_id: UUID
    start_time: datetime
    end_time: datetime
    location: str
    participants_count: int
    max_participants: Optional[int]
    is_online: bool
    cover_image: Optional[str]
    tags: List[str]
    status: str
    created_at: datetime
    updated_at: datetime
    is_registered: Optional[bool] = None

class EventListDTO(BaseCommunityDTO):
    events: List[EventResponseDTO]
    total_count: int
    page: int
    per_page: int