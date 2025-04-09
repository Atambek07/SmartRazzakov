# modules/community_hub/__init__.py
"""
CommunityHub Module - основной модуль для работы с сообществами

Содержит:
- Модели данных
- Бизнес-логику
- API endpoints
- Административные интерфейсы
"""

__version__ = '1.0.0'
__all__ = ['apps', 'admin', 'urls']

default_app_config = 'modules.community_hub.apps.CommunityHubConfig'