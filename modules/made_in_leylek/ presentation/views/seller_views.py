# modules/made_in_leylek/presentation/views/seller_views.py
from fastapi import APIRouter, Depends, HTTPException
from ...application.dto import (
    ProductCreateDTO,
    ProductUpdateDTO
)
from ...application.use_cases import ProductUseCase
from ..serializers import ProductResponseSerializer
from core.authentication import get_current_user

router = APIRouter(prefix="/seller", tags=["Seller"])

@router.post("/products", response_model=ProductResponseSerializer)
async def create_product(
    product_data: ProductCreateDTO,
    use_case: ProductUseCase = Depends(ProductUseCase),
    user: dict = Depends(get_current_user)
):
    """Добавление нового продукта"""
    try:
        product = await use_case.create_product(
            seller_id=user["id"],
            product_data=product_data
        )
        return ProductResponseSerializer(**product.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/products/{product_id}", response_model=ProductResponseSerializer)
async def update_product(
    product_id: str,
    product_data: ProductUpdateDTO,
    use_case: ProductUseCase = Depends(ProductUseCase),
    user: dict = Depends(get_current_user)
):
    """Обновление информации о продукте"""
    try:
        product = await use_case.update_product(
            seller_id=user["id"],
            product_id=product_id,
            update_data=product_data
        )
        return ProductResponseSerializer(**product.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))