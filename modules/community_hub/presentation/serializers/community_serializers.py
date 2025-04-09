# modules/community_hub/presentation/serializers/community_serializers.py
from rest_framework import serializers
from uuid import UUID
from typing import Optional, List
from ...domain.entities import Community
from . import BaseCommunitySerializer

class CommunitySerializer(BaseCommunitySerializer):
    """Сериализатор для списка сообществ"""
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=2000)
    category = serializers.ChoiceField(
        choices=Community.Category.choices
    )
    avatar_url = serializers.URLField(
        max_length=512,
        required=False,
        allow_null=True
    )
    members_count = serializers.IntegerField(
        min_value=0,
        read_only=True
    )
    is_public = serializers.BooleanField(default=True)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        default=list
    )
    created_at = serializers.DateTimeField(read_only=True)

    def validate_name(self, value: str) -> str:
        """Валидация названия сообщества"""
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Name must be at least 3 characters long"
            )
        return value.strip()

class CommunityDetailSerializer(CommunitySerializer):
    """Сериализатор для детальной информации о сообществе"""
    rules = serializers.CharField(
        max_length=5000,
        required=False,
        allow_null=True
    )
    location = serializers.CharField(
        max_length=100,
        required=False,
        allow_null=True
    )
    is_active = serializers.BooleanField(
        read_only=True
    )
    creator_id = serializers.UUIDField(
        read_only=True
    )

class CommunityCreateSerializer(CommunityDetailSerializer):
    """Сериализатор для создания сообщества"""
    def create(self, validated_data: Dict[str, Any]) -> Community:
        """Создание объекта сообщества"""
        from ...domain.entities import Community
        return Community(
            **validated_data,
            members_count=0,
            is_active=True
        )

    def to_representation(self, instance: Community) -> Dict:
        """Конвертация в формат для ответа"""
        return CommunityDetailSerializer(instance).data

class MemberSerializer(BaseCommunitySerializer):
    """Сериализатор для участников сообщества"""
    user_id = serializers.UUIDField(read_only=True)
    community_id = serializers.UUIDField(read_only=True)
    role = serializers.ChoiceField(
        choices=CommunityMember.Role.choices,
        default=CommunityMember.Role.MEMBER
    )
    joined_at = serializers.DateTimeField(read_only=True)
    contributions = serializers.IntegerField(
        min_value=0,
        read_only=True
    )
    badges = serializers.ListField(
        child=serializers.CharField(max_length=50),
        read_only=True
    )

class MemberRoleSerializer(serializers.Serializer):
    """Сериализатор для изменения роли участника"""
    role = serializers.ChoiceField(
        choices=CommunityMember.Role.choices,
        required=True
    )

    def validate_role(self, value: str) -> str:
        """Проверка допустимости роли"""
        if value == CommunityMember.Role.CREATOR:
            raise serializers.ValidationError(
                "Cannot set creator role directly"
            )
        return value