# modules/gov_connect/presentation/views/__init__.py
"""
Представления модуля GovConnect

Содержит:
- API для граждан
- API для муниципальных сотрудников
- Публичные дашборды
"""
from .citizen_views import router as citizen_router
from .municipal_views import router as municipal_router
from .public_dashboard import router as public_router

__all__ = ['citizen_router', 'municipal_router', 'public_router']