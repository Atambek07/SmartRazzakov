from rest_framework import serializers
from django.contrib.gis.geos import Point
from typing import List, Dict, Optional
from uuid import UUID

class RouteInputSerializer(serializers.Serializer):
    """Сериализатор для входящих данных маршрута"""
    start_lat = serializers.FloatField(min_value=-90, max_value=90)
    start_lon = serializers.FloatField(min_value=-180, max_value=180)
    end_lat = serializers.FloatField(min_value=-90, max_value=90)
    end_lon = serializers.FloatField(min_value=-180, max_value=180)
    transport_type = serializers.ChoiceField(
        choices=['bus', 'metro', 'bike', 'pedestrian', 'taxi']
    )
    avoid_tolls = serializers.BooleanField(default=False)
    wheelchair_accessible = serializers.BooleanField(default=False)

    def validate(self, data: Dict) -> Dict:
        """Дополнительная валидация координат"""
        if data['start_lat'] == data['end_lat'] and data['start_lon'] == data['end_lon']:
            raise serializers.ValidationError(
                "Start and end points cannot be identical"
            )
        return data

class RouteOutputSerializer(serializers.Serializer):
    """Сериализатор для исходящих данных маршрута"""
    id = serializers.UUIDField()
    start_point = serializers.ListField(
        child=serializers.FloatField(),
        min_length=2,
        max_length=2
    )
    end_point = serializers.ListField(
        child=serializers.FloatField(),
        min_length=2,
        max_length=2
    )
    waypoints = serializers.ListField(
        child=serializers.ListField(
            child=serializers.FloatField(),
            min_length=2,
            max_length=2
        )
    )
    distance_km = serializers.FloatField(min_value=0)
    estimated_duration_min = serializers.FloatField(min_value=0)
    transport_type = serializers.CharField()
    created_at = serializers.DateTimeField()
    eco_score = serializers.FloatField(
        min_value=0,
        max_value=10,
        allow_null=True
    )
    accessibility_features = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )

    def to_representation(self, instance: Dict) -> Dict:
        """Преобразование для API"""
        data = super().to_representation(instance)
        data['start_point'] = [instance.start_point[0], instance.start_point[1]]
        data['end_point'] = [instance.end_point[0], instance.end_point[1]]
        return data

class RouteUpdateSerializer(serializers.Serializer):
    """Сериализатор для обновления маршрута"""
    route_id = serializers.UUIDField()
    new_transport = serializers.ChoiceField(
        choices=['bus', 'metro', 'bike', 'pedestrian', 'taxi'],
        required=False
    )
    avoid_areas = serializers.ListField(
        child=serializers.ListField(
            child=serializers.FloatField(),
            min_length=2,
            max_length=2
        ),
        required=False
    )
    priority = serializers.ChoiceField(
        choices=['fastest', 'shortest', 'eco'],
        required=False
    )