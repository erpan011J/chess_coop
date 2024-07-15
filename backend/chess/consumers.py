import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room
from .redis_utils import RedisHandler
import logging

logger = logging.getLogger(__name__)

redis_instance = RedisHandler()

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
        message_type = data.get('type', 'move')

        handler = getattr(self, f'handle_{message_type}', self.handle_unknown)
        await handler(data)

    async def handle_move(self, data):
        move = data['move']
        fen = data['fen']
        turn = data['turn']
        
        redis_instance.update_fen(self.room_name, move, fen, turn)
         
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_chess_move',
                'move': move,
                'fen': fen,
                'turn': turn,
            }
        )

    async def handle_chat(self, data):
        message = data['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_chat_message',
                'message': message
            }
        )

    async def handle_player_joined(self, data):
        username = data['username']
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_player_joined',
                'username': username
            }
        )

    async def handle_player_left(self, data):
        username = data['username']
        redis_instance.reset_room(self.room_name, username)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_player_left',
                'username': username
            }
        )

    async def handle_unknown(self, data):
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': 'Unknown message type'
        }))

    async def send_chess_move(self, event):
        await self.send(text_data=json.dumps({
            'type': 'move',
            'move': event['move'],
            'fen': event['fen'],
            'turn': event['turn'],
        }))

    async def send_chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
        }))

    async def send_player_joined(self, event):
        await self.send(text_data=json.dumps({
            'type': 'player_joined',
            'username': event['username']
        }))

    async def send_player_left(self, event):
        await self.send(text_data=json.dumps({
            'type': 'player_left',
            'username': event['username']
        }))
