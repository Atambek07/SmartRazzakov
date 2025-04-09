# modules/feedback/presentation/serializers/rating_serializers.py
from rest_framework import serializers
from ...domain.entities import RatingSummary

class RatingSummarySerializer(serializers.Serializer):
    content_type = serializers.CharField()
    object_id = serializers.IntegerField()
    average_rating = serializers.FloatField()
    total_reviews = serializers.IntegerField()
    rating_distribution = serializers.DictField()
    confidence_score = serializers.FloatField(required=False)

    class Meta:
        model = RatingSummary
        fields = '__all__'

class ReviewVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewVote
        fields = ['vote_type', 'comment']
        extra_kwargs = {
            'comment': {'required': False}
        }