# modules/health_connect/presentation/serializers/medical_serializers.py
from rest_framework import serializers
from ...application.dto.medical_dto import (
    MedicalRecordCreate, 
    MedicalRecordUpdate,
    MedicalRecordResponse
)
from ...domain.entities import MedicalRecordType
from core.presentation.serializers import UserSerializer

class MedicalRecordCreateSerializer(serializers.Serializer):
    patient_id = serializers.UUIDField()
    record_type = serializers.ChoiceField(
        choices=MedicalRecordType.choices()
    )
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    date = serializers.DateTimeField()
    provider_id = serializers.UUIDField(required=False)
    is_confidential = serializers.BooleanField(default=False)
    attachments = serializers.ListField(
        child=serializers.FileField(),
        required=False
    )

    def validate_date(self, value):
        if value > timezone.now():
            raise serializers.ValidationError("Record date cannot be in the future")
        return value

    def create(self, validated_data):
        return MedicalRecordCreate(**validated_data)

class MedicalRecordUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False)
    record_type = serializers.ChoiceField(
        choices=MedicalRecordType.choices(),
        required=False
    )
    is_confidential = serializers.BooleanField(required=False)
    attachments = serializers.ListField(
        child=serializers.URLField(),
        required=False
    )

    def update(self, instance, validated_data):
        return MedicalRecordUpdate(**validated_data)

class MedicalRecordResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    patient = UserSerializer()
    record_type = serializers.ChoiceField(choices=MedicalRecordType.choices())
    title = serializers.CharField()
    description = serializers.CharField()
    date = serializers.DateTimeField()
    provider = UserSerializer(required=False)
    is_confidential = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField(required=False)
    attachments = serializers.ListField(
        child=serializers.URLField()
    )

    def to_dto(self, instance) -> MedicalRecordResponse:
        return MedicalRecordResponse(**instance)