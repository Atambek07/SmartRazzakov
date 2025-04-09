# modules/community_hub/presentation/consumers/chat_consumer.py
import json
from typing import Dict, Any
from uuid import UUID
from channels.db import database_sync_to_async
from django.core.exceptions import PermissionDenied
from .. import BaseCommunityConsumer
from infrastructure.repositories import MemberRepository
from domain.entities import ChatMessage
from domain.exceptions import CommunityNotFoundError


class ChatConsumer(BaseCommunityConsumer):
    """Consumer для чатов сообщества"""

    async def get_group_name(self):
        """Получение имени группы для комнаты чата"""
        community_id = self.scope['url_route']['kwargs']['community_id']
        return f"chat_{community_id}"

    async def process_message(self, data: Dict[str, Any]):
        """Обработка входящих сообщений чата"""
        message_type = data.get('type')

        if message_type == 'chat_message':
            await self.handle_chat_message(data)
        elif message_type == 'typing_indicator':
            await self.handle_typing_indicator(data)
        else:
            await self.send_error("Unknown message type")

    async def handle_chat_message(self, data: Dict[str, Any]):
        """Обработка сообщения чата"""
        community_id = UUID(self.scope['url_route']['kwargs']['community_id'])
        text = data.get('text', '').strip()

        if not text:
            await self.send_error("Message text cannot be empty")
            return

        try:
            # Проверка прав доступа
            if not await self.check_membership(community_id):
                raise PermissionDenied("Not a community member")

            # Создание сообщения
            message = await self.create_message(community_id, text)

            # Отправка сообщения в группу
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_id': str(message.id),
                    'user_id': str(self.user.id),
                    'username': self.user.username,
                    'text': text,
                    'timestamp': message.created_at.isoformat()
                }
            )
        except PermissionDenied:
            await self.send_error("You are not a member of this community", "permission_denied")
        except CommunityNotFoundError:
            await self.send_error("Community not found", "not_found")
        except Exception as e:
            logger.error(f"Error sending chat message: {str(e)}")
            await self.send_error("Failed to send message")

    async def handle_typing_indicator(self, data: Dict[str, Any]):
        """Обработка индикатора набора сообщения"""
        is_typing = data.get('is_typing', False)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_indicator',
                'user_id': str(self.user.id),
                'username': self.user.username,
                'is_typing': is_typing
            }
        )

    async def chat_message(self, event):
        """Отправка сообщения чата клиенту"""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message_id': event['message_id'],
            'user_id': event['user_id'],
            'username': event['username'],
            'text': event['text'],
            'timestamp': event['timestamp']
        }))

    async def typing_indicator(self, event):
        """Отправка индикатора набора сообщения"""
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user_id': event['user_id'],
            'username': event['username'],
            'is_typing': event['is_typing']
        }))

    @database_sync_to_async
    def check_membership(self, community_id: UUID) -> bool:
        """Проверка принадлежности пользователя к сообществу"""
        return MemberRepository().is_member(self.user.id, community_id)

    @database_sync_to_async
    def create_message(self, community_id: UUID, text: str) -> ChatMessage:
        """Создание сообщения чата в БД"""
        from infrastructure.models import ChatMessageModel
        message = ChatMessageModel.objects.create(
            community_id=community_id,
            user_id=self.user.id,
            text=text
        )
        return ChatMessage(
            id=message.id,
            community_id=message.community_id,
            user_id=message.user_id,
            text=message.text,
            created_at=message.created_at
        )