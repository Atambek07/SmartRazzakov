# modules/made_in_leylek/presentation/__init__.py
"""
Презентационный слой - содержит API endpoints, сериализаторы и представления
"""

from .urls import router
from .serializers import *
from .views import *

__all__ = [
    'router',
    'serializers',
    'views'
]