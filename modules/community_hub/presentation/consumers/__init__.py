# modules/community_hub/presentation/consumers/__init__.py
from abc import ABC, abstractmethod
from typing import Any, Dict
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from core.authentication import AuthMiddleware

logger = logging.getLogger(__name__)


class BaseCommunityConsumer(AsyncWebsocketConsumer, ABC):
    """Базовый consumer для WebSocket соединений"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.room_group_name = None

    async def connect(self):
        """Обработка подключения"""
        try:
            # Аутентификация пользователя
            self.user = await AuthMiddleware.authenticate_websocket(self.scope)
            if not self.user:
                await self.close(code=4001)
                return

            await self.accept()
            logger.info(f"WebSocket connected: {self.user.id}")

            # Присоединение к группе
            if hasattr(self, 'get_group_name'):
                self.room_group_name = await self.get_group_name()
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
        except Exception as e:
            logger.error(f"WebSocket connection error: {str(e)}")
            await self.close(code=4002)

    async def disconnect(self, close_code):
        """Обработка отключения"""
        if self.room_group_name:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        logger.info(f"WebSocket disconnected: {self.user.id if self.user else 'unknown'}")

    async def receive(self, text_data=None, bytes_data=None):
        """Обработка входящих сообщений"""
        try:
            if text_data:
                data = json.loads(text_data)
                await self.process_message(data)
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON format")
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await self.send_error("Internal server error")

    async def send_error(self, message: str, code: str = "error"):
        """Отправка сообщения об ошибке"""
        await self.send(json.dumps({
            "type": code,
            "message": message
        }))

    @abstractmethod
    async def process_message(self, data: Dict[str, Any]):
        """Обработка конкретных сообщений (должен быть реализован в подклассах)"""
        raise NotImplementedError