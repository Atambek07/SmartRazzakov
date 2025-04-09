# modules/community_hub/application/dto/chat_dto.py
from . import BaseCommunityDTO

class MessageDTO(BaseCommunityDTO):
    id: UUID
    sender_id: UUID
    content: str
    timestamp: datetime
    read_by: List[UUID]
    attachments: List[str]

class ChatChannelDTO(BaseCommunityDTO):
    id: UUID
    name: str
    description: Optional[str]
    is_private: bool
    members: List[UUID]
    last_message: Optional[MessageDTO]

class NotificationDTO(BaseCommunityDTO):
    id: UUID
    user_id: UUID
    title: str
    message: str
    is_read: bool
    created_at: datetime
    action_url: Optional[str]
    notification_type: str