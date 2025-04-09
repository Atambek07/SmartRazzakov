# modules/gov_connect/presentation/serializers/complaint_serializers.py
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField
from ...infrastructure.models import Complaint, ComplaintPhoto
from ...application.dto import ComplaintCreateDTO, ComplaintUpdateDTO
from core.api.serializers import UserPublicSerializer
import logging

logger = logging.getLogger(__name__)

class ComplaintPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintPhoto
        fields = ['photo_url', 'uploaded_at', 'is_approved']
        read_only_fields = ['uploaded_at', 'is_approved']

class ComplaintCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    location = GeometryField()
    category = serializers.CharField(max_length=50)
    photos = serializers.ListField(
        child=serializers.URLField(),
        max_length=5
    )
    anonymous = serializers.BooleanField(default=False)

    def validate_photos(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Необходимо хотя бы одно фото")
        return value

    def create(self, validated_data):
        try:
            return ComplaintCreateDTO(
                user_id=self.context['request'].user.id,
                title=validated_data['title'],
                description=validated_data['description'],
                location=validated_data['location'],
                category=validated_data['category'],
                photo_urls=validated_data['photos'],
                anonymous=validated_data['anonymous']
            )
        except Exception as e:
            logger.error(f"DTO creation error: {str(e)}")
            raise

class ComplaintUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=Complaint.Status.choices,
        required=False
    )
    municipal_comment = serializers.CharField(
        max_length=500, 
        required=False
    )
    before_photo = serializers.URLField(required=False)
    after_photo = serializers.URLField(required=False)

    def update(self, instance, validated_data):
        return ComplaintUpdateDTO(
            id=instance.id,
            **validated_data
        )

class ComplaintDetailSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    location = serializers.SerializerMethodField()
    photos = ComplaintPhotoSerializer(many=True)
    status_display = serializers.CharField(source='get_status_display')
    similar_complaints = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='complaint-detail'
    )

    class Meta:
        model = Complaint
        fields = [
            'id',
            'user',
            'title',
            'description',
            'location',
            'category',
            'status',
            'status_display',
            'created_at',
            'updated_at',
            'photos',
            'votes',
            'similar_complaints'
        ]
        read_only_fields = fields

    def get_location(self, obj):
        return {
            "type": "Point",
            "coordinates": [obj.location.x, obj.location.y]
        }