from rest_framework import serializers
from ..infrastructure.models import TransportRoute

class TransportRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportRoute
        fields = ['number', 'stops', 'schedule', 'price']

class RoutePlanSerializer(serializers.Serializer):
    start_point = serializers.CharField(max_length=100)
    end_point = serializers.CharField(max_length=100)
    optimization = serializers.ChoiceField(
        choices=[(tag.value, tag.name) for tag in RouteOptimization]
    )