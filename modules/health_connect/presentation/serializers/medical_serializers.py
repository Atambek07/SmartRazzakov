from rest_framework import serializers
from ..infrastructure.models import MedicalRecord

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['id', 'diagnosis', 'treatment', 'date', 'doctor', 'is_emergency']
        read_only_fields = ['date', 'doctor']

class EmergencySerializer(serializers.Serializer):
    patient_id = serializers.CharField()
    symptoms = serializers.CharField()
    location = serializers.CharField()
    severity = serializers.ChoiceField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])