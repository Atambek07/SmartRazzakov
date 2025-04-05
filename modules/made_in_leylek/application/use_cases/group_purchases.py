from ..domain.entities import GroupOrder
from ..domain.services import GroupPurchaseService


class CreateGroupOrderUseCase:
    def __init__(self, group_purchase_service: GroupPurchaseService):
        self.service = group_purchase_service

    def execute(self, product_id: str, target_quantity: int, initiator_id: str) -> GroupOrder:
        """Создает групповой заказ с проверкой условий"""
        if target_quantity < 10:
            raise ValueError("Минимальное количество для групповой покупки - 10 единиц")

        return self.service.create_group_order(
            product_id=product_id,
            target_quantity=target_quantity,
            initiator_id=initiator_id
        )