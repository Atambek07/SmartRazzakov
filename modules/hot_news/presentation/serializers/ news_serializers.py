from rest_framework import serializers
from ..infrastructure.models import NewsArticle

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = ['id', 'title', 'content', 'category', 'priority',
                 'publish_date', 'source', 'is_verified', 'image_url']
        read_only_fields = ['publish_date', 'is_verified']

class EmergencyAlertSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    message = serializers.CharField()
    location = serializers.CharField()
    priority = serializers.ChoiceField(
        choices=[(tag.value, tag.name) for tag in NewsPriority]
    )