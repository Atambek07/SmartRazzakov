# modules/made_in_leylek/presentation/serializers/order_serializers.py
from rest_framework import serializers
from decimal import Decimal
from ...application.dto.order_dto import (
    OrderCreateDTO,
    OrderResponseDTO,
    OrderStatusDTO,
    OrderStatus
)

class OrderItemSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01')
    )

class DeliveryInfoSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=255)
    pickup_point = serializers.CharField(
        max_length=100,
        required=False,
        allow_null=True
    )
    delivery_date = serializers.DateTimeField(required=False)
    contact_phone = serializers.CharField(max_length=20)

class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemSerializer(many=True, min_length=1)
    delivery = DeliveryInfoSerializer()
    buyer_comment = serializers.CharField(
        max_length=500,
        required=False,
        allow_null=True
    )

    def create(self, validated_data):
        return OrderCreateDTO(**validated_data)

class OrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=[(s.value, s.name) for s in OrderStatus]
    )
    admin_comment = serializers.CharField(
        max_length=500,
        required=False,
        allow_null=True
    )

    def to_dto(self) -> OrderStatusDTO:
        return OrderStatusDTO(**self.validated_data)

class OrderResponseSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    user_id = serializers.UUIDField()
    items = OrderItemSerializer(many=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    status = serializers.ChoiceField(
        choices=[(s.value, s.name) for s in OrderStatus]
    )
    delivery_info = DeliveryInfoSerializer()
    tracking_number = serializers.CharField(
        allow_null=True,
        required=False
    )
    buyer_comment = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def to_dto(self) -> OrderResponseDTO:
        return OrderResponseDTO(**self.validated_data)