# modules/community_hub/infrastructure/models/__init__.py
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from core.models import BaseModel

__all__ = [
    'CommunityModel',
    'CommunityMemberModel',
    'CommunityEventModel',
    'CommunityPostModel'
]