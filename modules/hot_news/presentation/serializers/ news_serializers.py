from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer
from core.api import DynamicFieldsMixin
from modules.hot_news.application.dto.news_dto import (
    NewsCreateDTO,
    NewsUpdateDTO,
    NewsResponseDTO
)
from modules.hot_news.infrastructure.models.news import NewsArticleModel

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Example Create',
            value={
                'title': 'Новый парк культуры',
                'content': 'Город объявляет о строительстве...',
                'category': 'culture',
                'priority': 2,
                'sources': ['https://gov.kg/official-news']
            },
            request_only=True
        )
    ]
)
class NewsCreateSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    category = serializers.ChoiceField(
        choices=NewsArticleModel.CategoryChoices.choices,
        help_text="Категория новости"
    )
    priority = serializers.IntegerField(
        min_value=1,
        max_value=4,
        default=2,
        help_text="Приоритет: 1-низкий, 4-критический"
    )
    sources = serializers.ListField(
        child=serializers.URLField(),
        max_length=5,
        allow_empty=False
    )

    class Meta:
        model = NewsArticleModel
        fields = [
            'title',
            'content',
            'category',
            'priority',
            'geo_location',
            'sources',
            'media_attachments'
        ]
        extra_kwargs = {
            'media_attachments': {'write_only': True}
        }

    def validate_sources(self, value):
        for source in value:
            if not any(source.startswith(prefix) 
                      for prefix in ['http', 'https', '/']):
                raise serializers.ValidationError(
                    "Источник должен быть URL или относительным путем"
                )
        return value

    def to_dto(self) -> NewsCreateDTO:
        return NewsCreateDTO(**self.validated_data)

class NewsUpdateSerializer(NewsCreateSerializer):
    class Meta(NewsCreateSerializer.Meta):
        model = NewsArticleModel
        extra_kwargs = {
            'title': {'required': False},
            'content': {'required': False},
            'category': {'required': False},
            'priority': {'required': False}
        }

    def to_dto(self) -> NewsUpdateDTO:
        return NewsUpdateDTO(**self.validated_data)

class NewsResponseSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display')
    priority = serializers.SerializerMethodField()
    author = serializers.StringRelatedField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticleModel
        fields = [
            'id',
            'title',
            'content',
            'category',
            'priority',
            'geo_location',
            'views_count',
            'created_at',
            'author',
            'status',
            'publish_at'
        ]
        read_only_fields = fields

    def get_priority(self, obj):
        return NewsArticleModel.PriorityChoices(obj.priority).label

    def get_status(self, obj):
        return 'Опубликовано' if obj.is_published else 'Черновик'

    def to_dto(self) -> NewsResponseDTO:
        return NewsResponseDTO(**self.data)