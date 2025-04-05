from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder


class CommunityChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.community_id = self.scope['url_route']['kwargs']['community_id']
        self.group_name = f'community_{self.community_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def receive_json(self, content, **kwargs):
        """Обрабатывает входящие сообщения"""
        message_type = content.get('type')

        if message_type == 'chat_message':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat.message',
                    'message': content['message'],
                    'sender': content['sender']
                }
            )

    async def chat_message(self, event):
        """Отправляет сообщение всем участникам группы"""
        await self.send_json(
            {
                'type': 'chat.message',
                'message': event['message'],
                'sender': event['sender'],
                'timestamp': datetime.now().isoformat()
            },
            cls=DjangoJSONEncoder
        )