# modules/made_in_leylek/application/use_cases/product_management.py
from decimal import Decimal
from typing import Optional, List
from ...domain.entities import ProductEntity, ProductCategory
from ...application.dto.product_dto import (
    ProductCreateDTO,
    ProductUpdateDTO,
    ProductResponseDTO,
    AuctionLotDTO
)
from ...domain.services import ProductService
from ....core.exceptions import NotFoundError, ValidationError

class ProductUseCases:
    def __init__(self, product_service: ProductService):
        self.product_service = product_service

    async def create_product(self, dto: ProductCreateDTO) -> ProductResponseDTO:
        """Создание нового продукта"""
        if dto.quantity < 0:
            raise ValidationError("Количество не может быть отрицательным")
        
        product = await self.product_service.create_product(
            seller_id=dto.seller_id,
            name=dto.name,
            description=dto.description,
            category=dto.category,
            price=dto.price,
            quantity=dto.quantity,
            production_date=dto.production_date,
            expiration_date=dto.expiration_date,
            tags=dto.tags
        )
        return self._convert_to_dto(product)

    async def update_product(self, product_id: str, dto: ProductUpdateDTO) -> ProductResponseDTO:
        """Обновление информации о продукте"""
        existing_product = await self.product_service.get_by_id(product_id)
        if not existing_product:
            raise NotFoundError("Продукт не найден")

        updated_product = await self.product_service.update_product(
            product_id=product_id,
            **dto.dict(exclude_unset=True)
        )
        return self._convert_to_dto(updated_product)

    async def list_products(
        self,
        category: Optional[ProductCategory] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
        search_query: Optional[str] = None
    ) -> List[ProductResponseDTO]:
        """Поиск и фильтрация продуктов"""
        products = await self.product_service.list_products(
            category=category,
            min_price=min_price,
            max_price=max_price,
            search_query=search_query
        )
        return [self._convert_to_dto(p) for p in products]

    async def create_auction_lot(self, dto: AuctionLotDTO) -> ProductResponseDTO:
        """Создание аукционного лота"""
        product = await self.product_service.get_by_id(dto.product_id)
        if not product:
            raise NotFoundError("Продукт не найден")
        
        if product.quantity < 1:
            raise ValidationError("Недостаточно товара для аукциона")
        
        auction_product = await self.product_service.create_auction(
            product_id=dto.product_id,
            start_price=dto.start_price,
            min_increment=dto.min_increment,
            start_time=dto.start_time,
            end_time=dto.end_time
        )
        return self._convert_to_dto(auction_product)

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