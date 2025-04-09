# modules/community_hub/application/dto/member_dto.py
from . import BaseCommunityDTO, MemberRole

class MemberDTO(BaseCommunityDTO):
    user_id: UUID
    community_id: UUID
    joined_at: datetime
    role: MemberRole
    contributions: int = Field(0, ge=0)
    last_active: Optional[datetime] = None
    badges: List[str] = Field(default_factory=list)

class MemberUpdateDTO(BaseCommunityDTO):
    role: MemberRole
    badges: Optional[List[str]] = None

class MemberListDTO(BaseCommunityDTO):
    members: List[MemberDTO]
    total_count: int
    page: int
    per_page: int

class PostCreateDTO(BaseCommunityDTO):
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=10, max_length=20000)
    tags: List[str] = Field(default_factory=list)
    is_pinned: bool = False
    attachments: List[HttpUrl] = Field(default_factory=list)

class PostResponseDTO(BaseCommunityDTO):
    id: UUID
    author_id: UUID
    community_id: UUID
    title: str
    content: str
    likes_count: int
    comments_count: int
    created_at: datetime
    updated_at: datetime
    tags: List[str]
    attachments: List[str]
    is_pinned: bool