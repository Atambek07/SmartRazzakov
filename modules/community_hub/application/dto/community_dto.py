# modules/community_hub/application/dto/community_dto.py
from datetime import datetime
from pydantic import validator, conint, constr
from typing import Optional, List
from . import BaseCommunityDTO, CommunityCategory, MemberRole

class CommunityCreateDTO(BaseCommunityDTO):
    name: constr(min_length=3, max_length=100, strip_whitespace=True)
    description: constr(min_length=10, max_length=2000)
    category: CommunityCategory
    is_public: bool = True
    rules: Optional[constr(max_length=5000)] = None
    avatar_url: Optional[HttpUrl] = None
    tags: List[constr(max_length=30)] = Field(default_factory=list)
    location: Optional[constr(max_length=100)] = None

    @validator('name')
    def validate_name(cls, v):
        if not any(c.isalpha() for c in v):
            raise ValueError("Name must contain at least one letter")
        if '  ' in v:
            raise ValueError("Name contains multiple spaces")
        return v.title()

class CommunityUpdateDTO(BaseCommunityDTO):
    name: Optional[constr(min_length=3, max_length=100)] = None
    description: Optional[constr(min_length=10, max_length=2000)] = None
    rules: Optional[constr(max_length=5000)] = None
    avatar_url: Optional[HttpUrl] = None
    is_public: Optional[bool] = None
    tags: Optional[List[constr(max_length=30)]] = None
    location: Optional[constr(max_length=100)] = None

class CommunityResponseDTO(BaseCommunityDTO):
    id: UUID
    name: str
    description: str
    category: CommunityCategory
    creator_id: UUID
    created_at: datetime
    updated_at: datetime
    members_count: conint(ge=0)
    is_public: bool
    rules: Optional[str]
    avatar_url: Optional[str]
    tags: List[str]
    location: Optional[str]
    is_member: Optional[bool] = None
    current_user_role: Optional[MemberRole] = None

class CommunityStatsDTO(BaseCommunityDTO):
    members_count: int
    active_members: int
    events_count: int
    posts_count: int
    last_activity: datetime

class CommunitySearchDTO(BaseCommunityDTO):
    query: Optional[str] = None
    categories: Optional[List[CommunityCategory]] = None
    tags: Optional[List[str]] = None
    is_public: Optional[bool] = None
    min_members: Optional[int] = None
    max_members: Optional[int] = None
    location: Optional[str] = None
    page: int = 1
    per_page: int = 20

class CommunityListDTO(BaseCommunityDTO):
    communities: List[CommunityResponseDTO]
    total_count: int
    page: int
    per_page: int