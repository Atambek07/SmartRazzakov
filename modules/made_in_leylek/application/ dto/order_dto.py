# modules/made_in_leylek/application/dto/order_dto.py
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, validator

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"

class OrderItemDTO(BaseModel):
    product_id: str = Field(..., min_length=1, description="Уникальный идентификатор продукта")
    quantity: int = Field(..., gt=0, description="Количество товара")
    price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Цена за единицу")

    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Цена должна быть больше нуля")
        return v

class DeliveryInfoDTO(BaseModel):
    address: str = Field(..., min_length=5, max_length=255, description="Адрес доставки")
    pickup_point: Optional[str] = Field(None, description="Пункт самовывоза")
    delivery_date: Optional[datetime] = Field(None, description="Предпочитаемая дата доставки")
    contact_phone: str = Field(..., regex=r"^\+?[1-9]\d{7,14}$", description="Контактный телефон")

class OrderCreateDTO(BaseModel):
    items: List[OrderItemDTO] = Field(..., min_items=1, description="Список товаров в заказе")
    delivery: DeliveryInfoDTO = Field(..., description="Информация о доставке")
    buyer_comment: Optional[str] = Field(None, max_length=500, description="Комментарий покупателя")

class OrderStatusDTO(BaseModel):
    status: OrderStatus = Field(..., description="Новый статус заказа")
    admin_comment: Optional[str] = Field(None, max_length=500, description="Комментарий администратора")

class OrderResponseDTO(OrderCreateDTO):
    order_id: str = Field(..., description="Уникальный идентификатор заказа")
    created_at: datetime = Field(..., description="Дата создания заказа")
    total_amount: Decimal = Field(..., description="Общая сумма заказа")
    current_status: OrderStatus = Field(..., description="Текущий статус заказа")
    tracking_number: Optional[str] = Field(None, description="Трек-номер для отслеживания")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: str(v)
        }