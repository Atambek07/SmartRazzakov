# modules/community_hub/application/dto/system_dto.py
from . import BaseCommunityDTO

class BadgeDTO(BaseCommunityDTO):
    id: UUID
    name: str
    description: str
    icon_url: str
    criteria: Dict[str, int]

class ReportDTO(BaseCommunityDTO):
    id: UUID
    reporter_id: UUID
    reason: str
    status: str
    created_at: datetime
    resolved_at: Optional[datetime]

class AnalyticsDTO(BaseCommunityDTO):
    active_members: int
    new_members: int
    events_created: int
    posts_created: int
    engagement_rate: float
    period_start: datetime
    period_end: datetime