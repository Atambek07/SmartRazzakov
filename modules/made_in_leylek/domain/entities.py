# modules/made_in_leylek/domain/entities.py
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Dict, Optional

class ProductCategory(str, Enum):
    FOOD = "food"
    HANDMADE = "handmade"
    AGRICULTURE = "agriculture"
    TEXTILE = "textile"
    CERAMICS = "ceramics"

class ProductEntity:
    def __init__(
        self,
        id: str,
        seller_id: str,
        name: str,
        description: str,
        category: ProductCategory,
        price: Decimal,
        quantity: int,
        production_date: datetime,
        expiration_date: Optional[datetime] = None,
        tags: List[str] = [],
        rating: float = 0.0,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now()
    ):
        self.id = id
        self.seller_id = seller_id
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.quantity = quantity
        self.production_date = production_date
        self.expiration_date = expiration_date
        self.tags = tags
        self.rating = rating
        self.created_at = created_at
        self.updated_at = updated_at

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderEntity:
    def __init__(
        self,
        id: str,
        user_id: str,
        items: List[Dict],
        total_amount: Decimal,
        status: OrderStatus,
        delivery_info: Dict,
        tracking_number: Optional[str] = None,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
        buyer_comment: Optional[str] = None
    ):
        self.id = id
        self.user_id = user_id
        self.items = items
        self.total_amount = total_amount
        self.status = status
        self.delivery_info = delivery_info
        self.tracking_number = tracking_number
        self.created_at = created_at
        self.updated_at = updated_at
        self.buyer_comment = buyer_comment

class AuctionStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class AuctionEntity:
    def __init__(
        self,
        id: str,
        product_id: str,
        start_price: Decimal,
        current_bid: Decimal,
        min_increment: Decimal,
        start_time: datetime,
        end_time: datetime,
        status: AuctionStatus,
        bids: List[Dict],
        created_at: datetime = datetime.now()
    ):
        self.id = id
        self.product_id = product_id
        self.start_price = start_price
        self.current_bid = current_bid
        self.min_increment = min_increment
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.bids = bids
        self.created_at = created_at

class GroupPurchaseStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    EXPIRED = "expired"

class GroupPurchaseEntity:
    def __init__(
        self,
        id: str,
        product_id: str,
        base_price: Decimal,
        current_participants: int,
        min_participants: int,
        end_time: datetime,
        status: GroupPurchaseStatus,
        discount_percent: Decimal,
        created_at: datetime = datetime.now()
    ):
        self.id = id
        self.product_id = product_id
        self.base_price = base_price
        self.current_participants = current_participants
        self.min_participants = min_participants
        self.end_time = end_time
        self.status = status
        self.discount_percent = discount_percent
        self.created_at = created_at