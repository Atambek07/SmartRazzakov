# modules/community_hub/infrastructure/integrations/realtime/websocket.py
import json
from typing import Dict, Any, Optional, Callable
from uuid import UUID
from .. import BaseRealtimeClient, RealtimeConnectionError
from websockets.client import connect as ws_connect
from websockets.exceptions import ConnectionClosed

class CommunityWebSocketClient(BaseRealtimeClient):
    def __init__(self, endpoint: str, token: str):
        self.endpoint = endpoint
        self.token = token
        self._ws = None
        self._message_handlers: Dict[str, Callable] = {}
        self._is_active = False

    async def connect(self):
        if self.is_connected:
            return

        try:
            self._ws = await ws_connect(
                f"{self.endpoint}?token={self.token}",
                ping_interval=30,
                ping_timeout=90
            )
            self._is_active = True
            asyncio.create_task(self._listen_messages())
        except Exception as e:
            raise RealtimeConnectionError(
                f"WebSocket connection failed: {str(e)}"
            ) from e

    async def _listen_messages(self):
        while self._is_active and self._ws:
            try:
                message = await self._ws.recv()
                await self._handle_message(message)
            except ConnectionClosed:
                self._is_active = False
                await self.connect()

    async def _handle_message(self, raw_message: str):
        try:
            message = json.loads(raw_message)
            handler = self._message_handlers.get(message.get('type'))
            if handler:
                await handler(message)
        except json.JSONDecodeError:
            print(f"Invalid JSON message: {raw_message}")

    def register_handler(self, message_type: str, handler: Callable):
        self._message_handlers[message_type] = handler

    async def send_message(self, message: Dict[str, Any]):
        if not self.is_connected:
            await self.connect()

        try:
            await self._ws.send(json.dumps(message))
        except ConnectionClosed:
            await self.connect()
            await self._ws.send(json.dumps(message))

    async def join_community_room(self, community_id: UUID):
        await self.send_message({
            "type": "join",
            "room": f"community_{community_id}"
        })

    async def leave_room(self, room: str):
        await self.send_message({
            "type": "leave",
            "room": room
        })

    @property
    def is_connected(self) -> bool:
        return self._ws is not None and not self._ws.closed

    async def disconnect(self):
        self._is_active = False
        if self._ws:
            await self._ws.close()
            self._ws = None