from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

class ProductCategory(Enum):
    HANDICRAFTS = "handicrafts"
    AGRICULTURE = "agriculture"
    TEXTILES = "textiles"
    FOOD = "food"

class OrderStatus(Enum):
    CREATED = "created"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

@dataclass
class Product:
    id: str
    title: str
    description: str
    category: ProductCategory
    price: float
    seller_id: str
    stock: int
    created_at: datetime
    is_auction: bool = False
    auction_end: Optional[datetime] = None

@dataclass
class GroupOrder:
    id: str
    product_id: str
    participants: List[str]
    target_quantity: int
    current_quantity: int
    discount: float
    expires_at: datetime