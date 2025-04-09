from rest_framework import serializers
from ...domain.entities import ContentType, CourseLevel
from ...infrastructure.models import (
    EducationalContentModel,
    CourseModel,
    TestResultModel
)

class ContentTypeField(serializers.Field):
    def to_representation(self, value):
        return ContentType(value).name.lower()

    def to_internal_value(self, data):
        try:
            return ContentType[data.upper()].value
        except KeyError:
            raise serializers.ValidationError("Invalid content type")

class EducationalContentSerializer(serializers.ModelSerializer):
    content_type = ContentTypeField()
    author = serializers.UUIDField(source='author.id')
    interactive_config = serializers.DictField(
        source='metadata.interactive_config',
        required=False
    )

    class Meta:
        model = EducationalContentModel
        fields = [
            'id',
            'title',
            'content_type',
            'subject',
            'grade_level',
            'author',
            'file_url',
            'interactive_config',
            'is_published',
            'created_at'
        ]
        extra_kwargs = {
            'file_url': {'required': True},
            'is_published': {'read_only': True}
        }

    def validate_grade_level(self, value):
        if not 1 <= value <= 11:
            raise serializers.ValidationError("Grade level must be between 1 and 11")
        return value

class CourseSerializer(serializers.ModelSerializer):
    level = serializers.ChoiceField(
        choices=CourseLevel.choices,
        source='get_level_display'
    )
    tutor = serializers.UUIDField(source='tutor.id')
    enrolled_students = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=EducationalContentModel.objects.all(),
        pk_field=serializers.UUIDField()
    )

    class Meta:
        model = CourseModel
        fields = [
            'id',
            'title',
            'tutor',
            'schedule',
            'price',
            'currency',
            'level',
            'capacity',
            'enrolled_students',
            'rating',
            'created_at'
        ]
        extra_kwargs = {
            'rating': {'read_only': True},
            'capacity': {'min_value': 1, 'max_value': 100}
        }

    def validate_schedule(self, value):
        required_keys = {'days', 'time', 'timezone'}
        if not all(key in value for key in required_keys):
            raise serializers.ValidationError("Invalid schedule format")
        return value