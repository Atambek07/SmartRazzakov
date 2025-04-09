# modules/community_hub/presentation/serializers/__init__.py
from rest_framework import serializers
from typing import Dict, Any, Optional
from uuid import UUID
from ..exceptions import SerializerValidationError

__all__ = [
    'CommunitySerializer',
    'CommunityDetailSerializer',
    'CommunityCreateSerializer',
    'EventSerializer',
    'EventCreateSerializer',
    'MemberSerializer',
    'MemberRoleSerializer'
]


class BaseCommunitySerializer(serializers.Serializer):
    """Базовый сериализатор с общими методами"""

    def to_uuid(self, value: str) -> UUID:
        """Конвертация строки в UUID с обработкой ошибок"""
        try:
            return UUID(value)
        except ValueError:
            raise SerializerValidationError(f"Invalid UUID: {value}")

    def validate_tags(self, tags: Optional[List[str]]) -> List[str]:
        """Валидация тегов"""
        if tags is None:
            return []

        if len(tags) > 15:
            raise serializers.ValidationError("Maximum 15 tags allowed")

        return [tag.lower().strip() for tag in tags if tag.strip()]