from rest_framework import serializers
from typing import Dict, Optional
from uuid import UUID

class TransportSerializer(serializers.Serializer):
    """Сериализатор для транспортных средств"""
    id = serializers.CharField()
    vehicle_type = serializers.ChoiceField(
        choices=['bus', 'metro', 'bike', 'taxi']
    )
    current_location = serializers.ListField(
        child=serializers.FloatField(),
        min_length=2,
        max_length=2
    )
    capacity = serializers.IntegerField(min_value=1)
    available = serializers.BooleanField()
    license_plate = serializers.CharField(
        allow_null=True,
        required=False
    )
    last_update = serializers.DateTimeField()
    properties = serializers.DictField(
        child=serializers.CharField(),
        allow_empty=True
    )

class TransportLocationSerializer(serializers.Serializer):
    """Сериализатор для обновления местоположения транспорта"""
    vehicle_id = serializers.CharField()
    lat = serializers.FloatField(min_value=-90, max_value=90)
    lon = serializers.FloatField(min_value=-180, max_value=180)
    speed = serializers.FloatField(min_value=0, required=False)
    timestamp = serializers.IntegerField(min_value=0)

    def validate(self, data: Dict) -> Dict:
        """Дополнительная валидация координат"""
        if abs(data['lat']) > 90 or abs(data['lon']) > 180:
            raise serializers.ValidationError(
                "Invalid coordinates values"
            )
        return data

class TransportTypeSerializer(serializers.Serializer):
    """Сериализатор для типов транспорта"""
    id = serializers.UUIDField()
    name = serializers.CharField()
    code = serializers.CharField()
    speed_kmh = serializers.FloatField(min_value=0)
    eco_class = serializers.IntegerField(min_value=0, max_value=5)
    icon = serializers.CharField()