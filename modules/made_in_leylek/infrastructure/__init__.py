# modules/made_in_leylek/infrastructure/__init__.py
"""
Инфраструктурный слой - реализация внешних интерфейсов:
- Базы данных (ORM модели)
- Внешние API
- Системы кеширования
- Брокеры сообщений
"""

from .models import Product, Order
from .repositories import ProductRepository, OrderRepository

__all__ = [
    'Product',
    'Order',
    'ProductRepository',
    'OrderRepository'
]