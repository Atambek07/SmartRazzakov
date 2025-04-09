# modules/community_hub/domain/entities.py
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import List, Optional, Dict, Set
from uuid import UUID, uuid4

class CommunityCategory(Enum):
    """Категории сообществ"""
    PROFESSIONAL = auto()
    HOBBY = auto()
    NEIGHBORHOOD = auto()
    CRISIS = auto()
    EDUCATION = auto()
    BUSINESS = auto()

class MemberRole(Enum):
    """Роли участников сообщества"""
    MEMBER = auto()
    MODERATOR = auto()
    ADMIN = auto()
    CREATOR = auto()

class EventStatus(Enum):
    """Статусы мероприятий"""
    PLANNED = auto()
    ONGOING = auto()
    COMPLETED = auto()
    CANCELLED = auto()

class PostStatus(Enum):
    """Статусы публикаций"""
    DRAFT = auto()
    PUBLISHED = auto()
    ARCHIVED = auto()
    REMOVED = auto()

@dataclass
class Community:
    """Основная сущность сообщества"""
    id: UUID = field(default_factory=uuid4)
    name: str
    description: str
    category: CommunityCategory
    creator_id: UUID
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    members_count: int = 0
    is_public: bool = True
    rules: Optional[str] = None
    avatar_url: Optional[str] = None
    tags: Set[str] = field(default_factory=set)
    location: Optional[str] = None
    is_active: bool = True

    def add_tag(self, tag: str):
        if len(self.tags) >= 15:  # Максимум 15 тегов
            raise ValueError("Maximum tags limit reached")
        self.tags.add(tag.lower())

@dataclass
class CommunityMember:
    """Участник сообщества"""
    user_id: UUID
    community_id: UUID
    joined_at: datetime = field(default_factory=datetime.utcnow)
    role: MemberRole = MemberRole.MEMBER
    contributions: int = 0
    last_active: Optional[datetime] = None
    badges: Set[str] = field(default_factory=set)

    def promote(self, new_role: MemberRole):
        if new_role.value <= self.role.value:
            raise ValueError("New role must be higher than current")
        self.role = new_role

@dataclass
class CommunityEvent:
    """Мероприятие сообщества"""
    id: UUID = field(default_factory=uuid4)
    community_id: UUID
    title: str
    description: str
    organizer_id: UUID
    start_time: datetime
    end_time: datetime
    location: str
    status: EventStatus = EventStatus.PLANNED
    max_participants: Optional[int] = None
    is_online: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    tags: Set[str] = field(default_factory=set)
    cover_image_url: Optional[str] = None

    def update_status(self, new_status: EventStatus):
        valid_transitions = {
            EventStatus.PLANNED: [EventStatus.ONGOING, EventStatus.CANCELLED],
            EventStatus.ONGOING: [EventStatus.COMPLETED]
        }
        if new_status not in valid_transitions.get(self.status, []):
            raise ValueError(f"Cannot transition from {self.status} to {new_status}")
        self.status = new_status

@dataclass
class CommunityPost:
    """Публикация в сообществе"""
    id: UUID = field(default_factory=uuid4)
    community_id: UUID
    author_id: UUID
    title: str
    content: str
    status: PostStatus = PostStatus.PUBLISHED
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    tags: Set[str] = field(default_factory=set)
    like_count: int = 0
    comment_count: int = 0
    is_pinned: bool = False
    moderator_id: Optional[UUID] = None
    moderation_reason: Optional[str] = None