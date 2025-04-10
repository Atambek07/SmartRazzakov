# modules/made_in_leylek/infrastructure/repositories/order_repo.py
from django.db import DatabaseError
from ...domain.entities import OrderEntity, OrderStatus
from ...domain.exceptions import OrderNotFoundError
from ..models.orders import Order

class OrderRepository:
    async def create(self, order: OrderEntity) -> OrderEntity:
        try:
            db_order = await Order.objects.acreate(
                id=order.id,
                user_id=order.user_id,
                items=order.items,
                total_amount=order.total_amount,
                status=order.status.value,
                delivery_info=order.delivery_info,
                tracking_number=order.tracking_number,
                buyer_comment=order.buyer_comment
            )
            return self._to_entity(db_order)
        except DatabaseError as e:
            raise OrderNotFoundError(f"Error creating order: {str(e)}")

    async def get_by_id(self, order_id: str) -> OrderEntity:
        try:
            db_order = await Order.objects.aget(id=order_id)
            return self._to_entity(db_order)
        except Order.DoesNotExist:
            raise OrderNotFoundError(f"Order {order_id} not found")

    async def update_status(self, order_id: str, status: OrderStatus) -> OrderEntity:
        try:
            db_order = await Order.objects.aget(id=order_id)
            db_order.status = status.value
            await db_order.asave()
            return self._to_entity(db_order)
        except Order.DoesNotExist:
            raise OrderNotFoundError(f"Order {order_id} not found")

    def _to_entity(self, db_order: Order) -> OrderEntity:
        return OrderEntity(
            id=str(db_order.id),
            user_id=str(db_order.user_id),
            items=db_order.items,
            total_amount=db_order.total_amount,
            status=OrderStatus(db_order.status),
            delivery_info=db_order.delivery_info,
            tracking_number=db_order.tracking_number,
            buyer_comment=db_order.buyer_comment,
            created_at=db_order.created_at,
            updated_at=db_order.updated_at
        )