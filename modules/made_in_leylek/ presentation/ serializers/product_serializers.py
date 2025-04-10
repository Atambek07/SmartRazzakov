# modules/made_in_leylek/presentation/serializers/product_serializers.py
from rest_framework import serializers
from decimal import Decimal
from ...application.dto.product_dto import (
    ProductCreateDTO,
    ProductUpdateDTO,
    ProductResponseDTO,
    ProductCategory
)

class ProductCategoryField(serializers.Field):
    def to_representation(self, value):
        return value.value

    def to_internal_value(self, data):
        try:
            return ProductCategory(data.lower())
        except ValueError:
            raise serializers.ValidationError(
                f"Invalid category. Valid choices: {[c.value for c in ProductCategory]}"
            )

class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    category = ProductCategoryField()
    price = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2,
        min_value=Decimal('0.01')
    )
    quantity = serializers.IntegerField(min_value=0)
    production_date = serializers.DateTimeField()
    expiration_date = serializers.DateTimeField(required=False)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        allow_empty=True
    )

    def create(self, validated_data):
        return ProductCreateDTO(**validated_data)

class ProductUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(required=False)
    category = ProductCategoryField(required=False)
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        required=False
    )
    quantity = serializers.IntegerField(min_value=0, required=False)
    expiration_date = serializers.DateTimeField(required=False)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False
    )

    def update(self, instance, validated_data):
        return ProductUpdateDTO(**validated_data)

class ProductResponseSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    seller_id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    category = ProductCategoryField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    production_date = serializers.DateTimeField()
    expiration_date = serializers.DateTimeField(allow_null=True)
    tags = serializers.ListField(child=serializers.CharField())
    rating = serializers.FloatField(min_value=0, max_value=5)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def to_dto(self) -> ProductResponseDTO:
        return ProductResponseDTO(**self.validated_data)