# modules/made_in_leylek/domain/services/logistics.py
from decimal import Decimal
from typing import Dict, Optional, List
from ....core.exceptions import (
    LogisticsError,
    InvalidLocationError
)
from ....core.logging import logger
from ..entities import OrderEntity

class LogisticsService:
    def __init__(
        self,
        delivery_repository,
        mapping_service,
        courier_adapters
    ):
        self.repo = delivery_repository
        self.mapping = mapping_service
        self.couriers = courier_adapters

    async def calculate_delivery_cost(
        self,
        order: OrderEntity,
        delivery_type: str
    ) -> Decimal:
        """Расчет стоимости доставки с учетом параметров"""
        self._validate_delivery_type(delivery_type)
        
        route = await self.mapping.calculate_route(
            from_address=order.warehouse_location,
            to_address=order.delivery_address
        )
        
        cost = self._base_cost_calculation(
            distance=route['distance'],
            weight=order.total_weight,
            delivery_type=delivery_type
        )
        
        return cost * Decimal("1.1")  # НДС

    async def arrange_delivery(
        self,
        order: OrderEntity,
        delivery_type: str
    ) -> Dict:
        """Организация доставки через выбранного провайдера"""
        try:
            courier = self.couriers[delivery_type]
            delivery_info = await courier.create_delivery(
                order_id=order.id,
                address=order.delivery_address,
                dimensions=self._get_package_dimensions(order)
            )
            
            await self.repo.save_tracking_info(
                order.id,
                delivery_info['tracking_number'],
                delivery_type
            )
            
            return delivery_info
        except KeyError:
            raise LogisticsError("Неизвестный тип доставки")
        except Exception as e:
            logger.error(f"Delivery failed: {str(e)}")
            raise LogisticsError("Ошибка организации доставки")

    async def track_package(self, tracking_number: str) -> Dict:
        """Отслеживание статуса доставки"""
        info = await self.repo.get_tracking_info(tracking_number)
        if not info:
            raise InvalidLocationError("Посылка не найдена")
            
        courier = self.couriers[info['delivery_type']]
        return await courier.track(tracking_number)

    def _validate_delivery_type(self, delivery_type: str):
        if delivery_type not in self.couriers:
            raise LogisticsError(f"Неподдерживаемый тип доставки: {delivery_type}")

    def _base_cost_calculation(
        self,
        distance: float,
        weight: float,
        delivery_type: str
    ) -> Decimal:
        base_rate = {
            "standard": Decimal("100"),
            "express": Decimal("200"),
            "pickup": Decimal("0")
        }.get(delivery_type, Decimal("150"))
        
        return base_rate + (Decimal(distance) * Decimal("0.5")) + (Decimal(weight) * Decimal("0.1"))

    def _get_package_dimensions(self, order: OrderEntity) -> Dict:
        return {
            "weight": order.total_weight,
            "volume": sum(item['volume'] for item in order.items),
            "items_count": len(order.items)
        }