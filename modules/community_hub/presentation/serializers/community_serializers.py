from rest_framework import serializers
from ..infrastructure.models import Community, CommunityMember


class CommunityMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = CommunityMember
        fields = ['username', 'role', 'joined_at', 'reputation']


class CommunitySerializer(serializers.ModelSerializer):
    members = CommunityMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'community_type', 'is_public', 'members']