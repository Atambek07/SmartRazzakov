# modules/made_in_leylek/application/use_cases/group_purchases.py
from decimal import Decimal
from typing import List, Dict
from ...domain.entities import ProductEntity
from ...application.dto.product_dto import ProductResponseDTO
from ...domain.services import GroupPurchaseService
from ....core.exceptions import ValidationError, NotFoundError

class GroupPurchaseUseCases:
    def __init__(self, group_service: GroupPurchaseService):
        self.group_service = group_service

    async def create_group_purchase(
        self,
        product_id: str,
        target_quantity: int,
        discount_percent: Decimal
    ) -> ProductResponseDTO:
        """Создание групповой покупки"""
        product = await self.group_service.get_product(product_id)
        if not product:
            raise NotFoundError("Продукт не найден")

        if target_quantity < 2:
            raise ValidationError("Минимальное количество для групповой покупки - 2")

        group_purchase = await self.group_service.create_group(
            product_id=product_id,
            target_quantity=target_quantity,
            discount_percent=discount_percent
        )
        return self._convert_to_dto(group_purchase)

    async def calculate_group_discount(
        self,
        product_id: str,
        participants: int
    ) -> Dict[str, Decimal]:
        """Расчет скидки для групповой покупки"""
        product = await self.group_service.get_product(product_id)
        if not product:
            raise NotFoundError("Продукт не найден")

        discount = await self.group_service.calculate_discount(
            product_id=product_id,
            current_participants=participants
        )
        return {
            "original_price": product.price,
            "discounted_price": product.price * (1 - discount),
            "discount_percent": discount * 100
        }

    def _convert_to_dto(self, product: ProductEntity) -> ProductResponseDTO:
        """Конвертация Entity в DTO"""
        return ProductResponseDTO(
            product_id=product.id,
            seller_id=product.seller_id,
            name=product.name,
            description=product.description,
            category=product.category,
            price=product.price,
            quantity=product.quantity,
            production_date=product.production_date,
            expiration_date=product.expiration_date,
            tags=product.tags,
            rating=product.rating,
            created_at=product.created_at,
            updated_at=product.updated_at
        )