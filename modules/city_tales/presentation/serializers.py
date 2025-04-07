from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from domain.entities import ContentFormat
from typing import Optional, List

class TaleContentSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=255)
    location_id = serializers.CharField()
    audio_url = serializers.URLField(required=False, allow_null=True)
    text_content = serializers.CharField(required=False, allow_null=True)
    images = serializers.ListField(
        child=serializers.URLField(),
        required=False,
        default=list
    )
    qr_code = serializers.CharField()
    format_preference = serializers.ChoiceField(
        choices=ContentFormat.choices(),
        required=False
    )

    def validate(self, data):
        """Проверяет наличие хотя бы одного формата контента."""
        if not any([data.get('audio_url'), data.get('text_content'), data.get('images')]):
            raise serializers.ValidationError(
                "Контент должен содержать хотя бы один формат (аудио, текст или изображения)"
            )
        return data

class QRRequestSerializer(serializers.Serializer):
    qr_code = serializers.CharField(max_length=64)
    user_id = serializers.CharField(
        max_length=36,
        required=False,
        help_text="ID пользователя для персонализации"
    )
    device_type = serializers.ChoiceField(
        choices=[("mobile", "Mobile"), ("desktop", "Desktop")],
        required=False
    )

class UserPreferenceSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    preferred_format = serializers.ChoiceField(choices=ContentFormat.choices())