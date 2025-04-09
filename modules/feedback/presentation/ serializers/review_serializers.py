# modules/feedback/presentation/serializers/review_serializers.py
from rest_framework import serializers
from ...application.dto import ReviewCreateDTO, ReviewResponseDTO
from ...domain.entities import ReviewEntity

class ReviewMediaSerializer(serializers.Serializer):
    audio = serializers.FileField(required=False)
    video = serializers.FileField(required=False)
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False
    )

class ReviewCreateSerializer(serializers.Serializer):
    content_type = serializers.CharField()
    object_id = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField(required=False, allow_blank=True)
    media = ReviewMediaSerializer(required=False)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False
    )

    def create(self, validated_data):
        return ReviewCreateDTO(**validated_data)

class ReviewResponseSerializer(serializers.ModelSerializer):
    media = ReviewMediaSerializer()
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        read_only=True
    )
    author = serializers.StringRelatedField()
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id',
            'author',
            'content_type',
            'object_id',
            'content_object',
            'rating',
            'text',
            'media',
            'tags',
            'status',
            'helpful_count',
            'created_at'
        ]
        read_only_fields = fields

    def get_content_object(self, obj):
        # Динамическая сериализация связанного объекта
        from core.api.serializers import ContentObjectSerializer
        return ContentObjectSerializer(obj.content_object).data

class ReviewFilterSerializer(serializers.Serializer):
    min_rating = serializers.IntegerField(min_value=1, max_value=5, required=False)
    content_type = serializers.CharField(required=False)
    has_media = serializers.BooleanField(required=False)
    tags = serializers.CharField(required=False)