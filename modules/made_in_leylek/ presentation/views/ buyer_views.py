# modules/made_in_leylek/presentation/views/buyer_views.py
from fastapi import APIRouter, Depends, HTTPException
from ...application.dto import (
    OrderCreateDTO,
    GroupPurchaseJoinDTO
)
from ...application.use_cases import (
    OrderUseCase,
    GroupPurchaseUseCase
)
from ..serializers import (
    OrderResponseSerializer,
    GroupPurchaseSerializer
)
from core.authentication import get_current_user

router = APIRouter(prefix="/buyer", tags=["Buyer"])

@router.post("/orders", response_model=OrderResponseSerializer)
async def create_order(
    order_data: OrderCreateDTO,
    use_case: OrderUseCase = Depends(OrderUseCase),
    user: dict = Depends(get_current_user)
):
    """Создание нового заказа"""
    try:
        order = await use_case.create_order(
            user_id=user["id"],
            items=order_data.items,
            delivery_info=order_data.delivery
        )
        return OrderResponseSerializer(**order.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/group-purchases/{group_id}/join")
async def join_group_purchase(
    group_id: str,
    data: GroupPurchaseJoinDTO,
    use_case: GroupPurchaseUseCase = Depends(GroupPurchaseUseCase),
    user: dict = Depends(get_current_user)
):
    """Присоединение к групповой покупке"""
    try:
        result = await use_case.join_group(
            user_id=user["id"],
            group_id=group_id,
            quantity=data.quantity
        )
        return {"status": "success", "message": "Joined group purchase"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))