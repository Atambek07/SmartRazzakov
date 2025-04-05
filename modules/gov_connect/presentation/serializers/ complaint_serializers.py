from rest_framework import serializers
from ..infrastructure.models import CitizenComplaint

class CitizenComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenComplaint
        fields = ['id', 'title', 'description', 'status', 'priority', 'created_at']
        read_only_fields = ['status', 'priority', 'created_at']

class ComplaintPhotoSerializer(serializers.Serializer):
    photo = serializers.ImageField()
    location = serializers.CharField()

class ComplaintStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=CitizenComplaint.STATUS_CHOICES)
    comment = serializers.CharField(required=False)