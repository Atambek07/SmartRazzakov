from rest_framework import serializers
from ..infrastructure.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'target_id', 'feedback_type', 'text', 'rating', 'photos']
        read_only_fields = ['status', 'created_at']

class RatingSerializer(serializers.Serializer):
    target_id = serializers.CharField()
    average = serializers.FloatField()
    count = serializers.IntegerField()
    last_updated = serializers.DateTimeField()