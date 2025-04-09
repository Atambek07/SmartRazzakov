# modules/gov_connect/presentation/serializers/service_serializers.py
from rest_framework import serializers
from ...infrastructure.models import ServiceCategory, GovernmentService
from core.api.serializers import DynamicFieldsMixin
from django.utils.translation import gettext_lazy as _

class ServiceCategorySerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['slug', 'name', 'description']
        read_only_fields = ['slug']

class GovernmentServiceSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    category = ServiceCategorySerializer()
    rating = serializers.FloatField(source='average_rating')
    next_available_slot = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = GovernmentService
        fields = [
            'id',
            'name',
            'category',
            'description',
            'required_documents',
            'online_available',
            'rating',
            'next_available_slot'
        ]
        read_only_fields = ['rating', 'next_available_slot']

class BookingSlotSerializer(serializers.Serializer):
    office_id = serializers.UUIDField()
    service_id = serializers.UUIDField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    capacity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError(_("End time must be after start time"))
        return data