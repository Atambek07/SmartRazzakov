# modules/made_in_leylek/application/mappers.py
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Type
from pydantic import BaseModel
from ...domain.entities import (
    ProductEntity,
    AuctionEntity,
    OrderEntity,
    GroupPurchaseEntity
)
from .dto import (
    ProductResponseDTO,
    ProductCreateDTO,
    ProductUpdateDTO,
    AuctionLotDTO,
    OrderResponseDTO,
    OrderCreateDTO,
    GroupPurchaseDTO
)

class Mapper:
    @classmethod
    def to_dto(cls, entity: BaseModel, dto_class: Type[BaseModel]) -> BaseModel:
        raise NotImplementedError

    @classmethod
    def to_entity(cls, dto: BaseModel) -> BaseModel:
        raise NotImplementedError

class ProductMapper(Mapper):
    @classmethod
    def to_dto(cls, product: ProductEntity) -> ProductResponseDTO:
        return ProductResponseDTO(
            product_id=str(product.id),
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

    @classmethod
    def from_create_dto(cls, dto: ProductCreateDTO) -> ProductEntity:
        return ProductEntity(
            id=None,
            seller_id=dto.seller_id,
            name=dto.name,
            description=dto.description,
            category=dto.category,
            price=dto.price,
            quantity=dto.quantity,
            production_date=dto.production_date,
            expiration_date=dto.expiration_date,
            tags=dto.tags,
            rating=0.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    @classmethod
    def from_update_dto(cls, entity: ProductEntity, dto: ProductUpdateDTO) -> ProductEntity:
        return ProductEntity(
            id=entity.id,
            seller_id=entity.seller_id,
            name=dto.name or entity.name,
            description=dto.description or entity.description,
            category=dto.category or entity.category,
            price=dto.price or entity.price,
            quantity=dto.quantity or entity.quantity,
            production_date=dto.production_date or entity.production_date,
            expiration_date=dto.expiration_date or entity.expiration_date,
            tags=dto.tags or entity.tags,
            rating=entity.rating,
            created_at=entity.created_at,
            updated_at=datetime.now()
        )

class AuctionMapper(Mapper):
    @classmethod
    def to_dto(cls, auction: AuctionEntity) -> AuctionLotDTO:
        return AuctionLotDTO(
            product_id=str(auction.product_id),
            start_price=auction.start_price,
            min_increment=auction.min_increment,
            start_time=auction.start_time,
            end_time=auction.end_time,
            current_bid=auction.current_bid,
            status=auction.status
        )

    @classmethod
    def from_dto(cls, dto: AuctionLotDTO) -> AuctionEntity:
        return AuctionEntity(
            id=None,
            product_id=dto.product_id,
            start_price=dto.start_price,
            min_increment=dto.min_increment,
            start_time=dto.start_time,
            end_time=dto.end_time,
            current_bid=None,
            status="pending",
            created_at=datetime.now()
        )

class OrderMapper(Mapper):
    @classmethod
    def to_dto(cls, order: OrderEntity) -> OrderResponseDTO:
        return OrderResponseDTO(
            order_id=str(order.id),
            items=order.items,
            delivery_info=order.delivery_info,
            total_amount=order.total_amount,
            status=order.status,
            buyer_comment=order.buyer_comment,
            created_at=order.created_at,
            updated_at=order.updated_at,
            tracking_number=order.tracking_number
        )

    @classmethod
    def from_create_dto(cls, dto: OrderCreateDTO) -> OrderEntity:
        return OrderEntity(
            id=None,
            user_id=dto.user_id,
            items=dto.items,
            delivery_info=dto.delivery_info,
            total_amount=sum(item['price'] * item['quantity'] for item in dto.items),
            status="pending",
            buyer_comment=dto.buyer_comment,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            tracking_number=None
        )

class GroupPurchaseMapper(Mapper):
    @classmethod
    def to_dto(cls, group: GroupPurchaseEntity) -> GroupPurchaseDTO:
        return GroupPurchaseDTO(
            group_id=str(group.id),
            product_id=group.product_id,
            base_price=group.base_price,
            current_participants=group.current_participants,
            min_participants=group.min_participants,
            end_time=group.end_time,
            status=group.status,
            created_at=group.created_at,
            discount_percent=group.discount_percent
        )

    @classmethod
    def from_dto(cls, dto: GroupPurchaseDTO) -> GroupPurchaseEntity:
        return GroupPurchaseEntity(
            id=None,
            product_id=dto.product_id,
            base_price=dto.base_price,
            current_participants=0,
            min_participants=dto.min_participants,
            end_time=dto.end_time,
            status="active",
            created_at=datetime.now(),
            discount_percent=0.0
        )

class DatabaseMapper:
    @staticmethod
    def product_to_orm(entity: ProductEntity) -> Dict:
        return {
            "seller_id": entity.seller_id,
            "name": entity.name,
            "description": entity.description,
            "category": entity.category.value,
            "price": float(entity.price),
            "quantity": entity.quantity,
            "production_date": entity.production_date,
            "expiration_date": entity.expiration_date,
            "tags": entity.tags,
            "rating": entity.rating,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at
        }

    @staticmethod
    def product_from_orm(orm_obj) -> ProductEntity:
        return ProductEntity(
            id=str(orm_obj.id),
            seller_id=orm_obj.seller_id,
            name=orm_obj.name,
            description=orm_obj.description,
            category=orm_obj.category,
            price=Decimal(orm_obj.price),
            quantity=orm_obj.quantity,
            production_date=orm_obj.production_date,
            expiration_date=orm_obj.expiration_date,
            tags=orm_obj.tags,
            rating=orm_obj.rating,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at
        )