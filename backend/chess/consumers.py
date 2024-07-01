import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room

class ChessConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'room_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        move = data['move']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chess_move',
                'move': move
            }
        )

    async def chess_move(self, event):
        move = event['move']

        await self.send(text_data=json.dumps({
            'move': move
        }))
