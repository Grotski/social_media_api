import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope["user"].username
        self.recipien = self.scope["url_route"]["kwargs"]["username"]
        await self.accept()