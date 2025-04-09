# modules/health_connect/presentation/serializers/appointment_serializers.py
from rest_framework import serializers
from ...application.dto.appointment_dto import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse
)
from ...domain.entities import AppointmentStatus
from core.presentation.serializers import UserSerializer

class AppointmentCreateSerializer(serializers.Serializer):
    patient_id = serializers.UUIDField()
    provider_id = serializers.UUIDField()
    scheduled_time = serializers.DateTimeField()
    reason = serializers.CharField(
        max_length=500, 
        required=False
    )
    notes = serializers.CharField(
        max_length=1000, 
        required=False
    )

    def validate_scheduled_time(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                "Appointment time must be in the future"
            )
        return value

    def create(self, validated_data):
        return AppointmentCreate(**validated_data)

class AppointmentUpdateSerializer(serializers.Serializer):
    scheduled_time = serializers.DateTimeField(required=False)
    status = serializers.ChoiceField(
        choices=AppointmentStatus.choices(),
        required=False
    )
    reason = serializers.CharField(required=False)
    notes = serializers.CharField(required=False)

    def validate_scheduled_time(self, value):
        if value and value <= timezone.now():
            raise serializers.ValidationError(
                "Updated time must be in the future"
            )
        return value

    def update(self, instance, validated_data):
        return AppointmentUpdate(**validated_data)

class AppointmentResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    patient = UserSerializer()
    provider = UserSerializer()
    scheduled_time = serializers.DateTimeField()
    status = serializers.ChoiceField(choices=AppointmentStatus.choices())
    duration = serializers.IntegerField(min_value=15, max_value=120)
    reason = serializers.CharField(required=False)
    notes = serializers.CharField(required=False)
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField(required=False)
    video_link = serializers.URLField(required=False)

    def to_dto(self, instance) -> AppointmentResponse:
        return AppointmentResponse(**instance)
    