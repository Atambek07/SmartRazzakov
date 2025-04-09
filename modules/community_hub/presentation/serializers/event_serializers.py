# modules/community_hub/presentation/serializers/event_serializers.py
from rest_framework import serializers
from datetime import datetime
from uuid import UUID
from typing import Optional
from ...domain.entities import CommunityEvent
from . import BaseCommunitySerializer


class EventSerializer(BaseCommunitySerializer):
    """Сериализатор для мероприятий"""
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=10000)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    location = serializers.CharField(max_length=200)
    status = serializers.ChoiceField(
        choices=CommunityEvent.Status.choices,
        read_only=True
    )
    max_participants = serializers.IntegerField(
        min_value=1,
        required=False,
        allow_null=True
    )
    is_online = serializers.BooleanField(default=False)
    cover_image_url = serializers.URLField(
        max_length=512,
        required=False,
        allow_null=True
    )
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        default=list
    )
    community_id = serializers.UUIDField(read_only=True)
    organizer_id = serializers.UUIDField(read_only=True)

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Валидация временных промежутков"""
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError(
                "End time must be after start time"
            )

        if start_time and start_time < datetime.now():
            raise serializers.ValidationError(
                "Start time cannot be in the past"
            )

        return data


class EventCreateSerializer(EventSerializer):
    """Сериализатор для создания мероприятий"""

    def create(self, validated_data: Dict[str, Any]) -> CommunityEvent:
        """Создание объекта мероприятия"""
        from ...domain.entities import CommunityEvent
        return CommunityEvent(
            **validated_data,
            status=CommunityEvent.Status.PLANNED
        )