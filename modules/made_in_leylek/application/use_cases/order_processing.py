# modules/made_in_leylek/application/use_cases/order_processing.py
from decimal import Decimal
from typing import List, Optional
from ...domain.entities import OrderEntity
from ...application.dto.order_dto import (
    OrderCreateDTO,
    OrderResponseDTO,
    OrderStatusDTO,
    OrderStatus
)
from ...domain.services import OrderService, PaymentService, LogisticsService
from ....core.exceptions import (
    NotFoundError,
    ValidationError,
    InsufficientStockError
)

class OrderUseCases:
    def __init__(
        self,
        order_service: OrderService,
        payment_service: PaymentService,
        logistics_service: LogisticsService
    ):
        self.order_service = order_service
        self.payment_service = payment_service
        self.logistics_service = logistics_service

    async def create_order(self, dto: OrderCreateDTO) -> OrderResponseDTO:
        """Создание нового заказа"""
        # Проверка доступности товаров
        for item in dto.items:
            product = await self.order_service.get_product(item.product_id)
            if product.quantity < item.quantity:
                raise InsufficientStockError(
                    f"Недостаточно товара {product.name} на складе"
                )

        # Создание заказа
        order = await self.order_service.create_order(
            items=[i.dict() for i in dto.items],
            delivery_info=dto.delivery.dict(),
            buyer_comment=dto.buyer_comment
        )

        # Инициализация оплаты
        payment_result = await self.payment_service.process_payment(
            order_id=order.id,
            amount=order.total_amount
        )

        if not payment_result.success:
            await self.order_service.cancel_order(order.id)
            raise ValidationError("Оплата не прошла")

        # Организация доставки
        tracking_info = await self.logistics_service.arrange_delivery(
            order_id=order.id,
            delivery_data=dto.delivery.dict()
        )

        return self._convert_to_dto(order, tracking_info)

    async def update_order_status(
        self,
        order_id: str,
        dto: OrderStatusDTO
    ) -> OrderResponseDTO:
        """Обновление статуса заказа"""
        order = await self.order_service.get_order(order_id)
        if not order:
            raise NotFoundError("Заказ не найден")

        updated_order = await self.order_service.update_status(
            order_id=order_id,
            new_status=dto.status,
            comment=dto.admin_comment
        )
        return self._convert_to_dto(updated_order)

    def _convert_to_dto(
        self,
        order: OrderEntity,
        tracking_info: Optional[dict] = None
    ) -> OrderResponseDTO:
        """Конвертация Entity в DTO"""
        return OrderResponseDTO(
            order_id=order.id,
            items=order.items,
            delivery=order.delivery_info,
            buyer_comment=order.buyer_comment,
            created_at=order.created_at,
            total_amount=order.total_amount,
            current_status=order.status,
            tracking_number=tracking_info.get("tracking_number") if tracking_info else None
        )