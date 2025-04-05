from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

class CommunityType(Enum):
    PROFESSIONAL = "professional"
    HOBBY = "hobby"
    NEIGHBORHOOD = "neighborhood"
    CRISIS = "crisis"

class MemberRole(Enum):
    OWNER = "owner"
    MODERATOR = "moderator"
    MEMBER = "member"

@dataclass
class Community:
    id: str
    name: str
    description: str
    community_type: CommunityType
    members: List['CommunityMember']
    created_at: datetime
    is_public: bool = True
    rules: Optional[str] = None

@dataclass
class CommunityMember:
    user_id: str
    role: MemberRole
    joined_at: datetime
    reputation_score: int = 0