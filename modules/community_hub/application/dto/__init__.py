# modules/community_hub/application/dto/__init__.py
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Union
from uuid import UUID

class BaseCommunityDTO(BaseModel):
    """Базовый класс для всех DTO с общими настройками"""
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
        extra = "forbid"  # Запрет дополнительных полей
        validate_assignment = True

class CommunityCategory(str, Enum):
    PROFESSIONAL = "professional"
    HOBBY = "hobby"
    CRISIS = "crisis"
    NEIGHBORHOOD = "neighborhood"
    EDUCATION = "education"
    BUSINESS = "business"

class MemberRole(str, Enum):
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"
    CREATOR = "creator"