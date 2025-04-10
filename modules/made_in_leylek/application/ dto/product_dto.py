# modules/made_in_leylek/application/dto/product_dto.py
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, validator

class ProductCategory(str, Enum):
    FOOD = "food"
    HANDMADE = "handmade"
    AGRICULTURE = "agriculture"
    TEXTILE = "textile"
    CERAMICS = "ceramics"

class ProductBaseDTO(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Название продукта")
    description: str = Field(..., min_length=10, max_length=1000, description="Описание продукта")
    category: ProductCategory = Field(..., description="Категория продукта")
    price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Цена за единицу")
    quantity: int = Field(..., ge=0, description="Доступное количество")
    production_date: datetime = Field(..., description="Дата производства")
    expiration_date: Optional[datetime] = Field(None, description="Срок годности (если применимо)")
    tags: List[str] = Field([], description="Теги для поиска")

    @validator('expiration_date')
    def validate_expiration_date(cls, v, values):
        if v and 'production_date' in values and v <= values['production_date']:
            raise ValueError("Срок годности должен быть после даты производства")
        return v

class ProductCreateDTO(ProductBaseDTO):
    seller_id: str = Field(..., min_length=1, description="Идентификатор продавца")

class ProductUpdateDTO(ProductBaseDTO):
    pass

class ProductResponseDTO(ProductCreateDTO):
    product_id: str = Field(..., description="Уникальный идентификатор продукта")
    rating: float = Field(0.0, ge=0, le=5.0, description="Рейтинг продукта")
    created_at: datetime = Field(..., description="Дата создания записи")
    updated_at: datetime = Field(..., description="Дата последнего обновления")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: str(v)
        }

class AuctionLotDTO(BaseModel):
    product_id: str = Field(..., description="Идентификатор продукта")
    start_price: Decimal = Field(..., gt=0, description="Начальная цена")
    min_increment: Decimal = Field(..., gt=0, description="Минимальный шаг ставки")
    start_time: datetime = Field(..., description="Время начала аукциона")
    end_time: datetime = Field(..., description="Время окончания аукциона")

    @validator('end_time')
    def validate_end_time(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError("Время окончания аукциона должно быть позже времени начала")
        return v