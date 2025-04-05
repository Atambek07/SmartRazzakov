from rest_framework import serializers
from .infrastructure.models import StoryModel

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryModel
        fields = ['id', 'title', 'content_type', 'location', 'qr_code']
        read_only_fields = ['qr_code']

class StoryDetailSerializer(serializers.ModelSerializer):
    audio_url = serializers.SerializerMethodField()

    class Meta:
        model = StoryModel
        fields = '__all__'

    def get_audio_url(self, obj):
        if obj.content.get('audio'):
            return self.context['request'].build_absolute_uri(obj.content['audio'])
        return None