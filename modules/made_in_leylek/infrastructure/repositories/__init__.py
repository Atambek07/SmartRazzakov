# modules/made_in_leylek/infrastructure/repositories/__init__.py
from .product_repo import ProductRepository
from .order_repo import OrderRepository

__all__ = ['ProductRepository', 'OrderRepository']