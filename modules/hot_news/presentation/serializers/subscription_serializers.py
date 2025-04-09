from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer
from core.api import DynamicFieldsMixin
from modules.hot_news.application.dto.subscription_dto import (
    SubscriptionCreateDTO,
    SubscriptionUpdateDTO,
    SubscriptionResponseDTO
)
from modules.hot_news.infrastructure.models.subscriptions import NewsSubscriptionModel

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Subscription Example',
            value={
                'categories': ['transport', 'emergency'],
                'notify_by_email': True,
                'preferred_language': 'ru'
            }
        )
    ]
)
class SubscriptionSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    categories = serializers.MultipleChoiceField(
        choices=NewsSubscriptionModel._meta.get_field('categories').choices,
        help_text="Выберите минимум одну категорию"
    )
    notify_by_email = serializers.BooleanField(default=False)
    notify_by_push = serializers.BooleanField(default=True)
    notify_by_sms = serializers.BooleanField(default=False)

    class Meta:
        model = NewsSubscriptionModel
        fields = [
            'categories',
            'notify_by_email',
            'notify_by_push',
            'notify_by_sms',
            'preferred_language'
        ]
        extra_kwargs = {
            'preferred_language': {
                'help': 'Язык уведомлений: ru, ky, en'
            }
        }

    def validate(self, attrs):
        if not any([attrs.get('notify_by_email'), 
                   attrs.get('notify_by_push'),
                   attrs.get('notify_by_sms')]):
            raise serializers.ValidationError(
                "Выберите хотя бы один канал уведомлений"
            )
        return attrs

    def to_dto(self, user_id: str) -> SubscriptionCreateDTO:
        return SubscriptionCreateDTO(
            user_id=user_id,
            **self.validated_data
        )

class SubscriptionResponseSerializer(SubscriptionSerializer):
    status = serializers.CharField(source='get_is_active_display')

    class Meta(SubscriptionSerializer.Meta):
        model = NewsSubscriptionModel
        fields = SubscriptionSerializer.Meta.fields + ['status', 'created_at']
        read_only_fields = fields

    def to_dto(self) -> SubscriptionResponseDTO:
        return SubscriptionResponseDTO(**self.data)