# modules/community_hub/apps.py
from django.apps import AppConfig


class CommunityHubConfig(AppConfig):
    """Конфигурация приложения CommunityHub"""

    name = 'modules.community_hub'
    verbose_name = 'Community Hub'

    def ready(self):
        """Инициализация приложения"""
        # Импорт сигналов и других обработчиков
        from . import signals  # noqa
        self.register_admin_models()

    def register_admin_models(self):
        """Автоматическая регистрация моделей в админке"""
        from django.contrib import admin
        from .models import (
            CommunityModel,
            CommunityMemberModel,
            CommunityEventModel,
            CommunityPostModel
        )

        admin.site.register(CommunityModel)
        admin.site.register(CommunityMemberModel)
        admin.site.register(CommunityEventModel)
        admin.site.register(CommunityPostModel)