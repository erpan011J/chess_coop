import json
import logging
from .redis_config import get_redis_connection
from .custom_exceptions import RoomNotFoundError, RoomFullError, InvalidInputError

logger = logging.getLogger(__name__)

class RedisHandler:
    def __init__(self):
        self.redis_instance = get_redis_connection()

    def room_exists(self, room_name):
        redis_key = f"room:{room_name}"
        return self.redis_instance.exists(redis_key)

    def create_room(self, room_name, creator):
        if not room_name or not creator:
            raise InvalidInputError("Room name and creator are required")

        redis_key = f"room:{room_name}"
        if self.room_exists(room_name):
            raise InvalidInputError(f"Room {room_name} already exists")

        initial_room_data = {
            "room_name": room_name,
            "creator": creator,
            "players": "1",
            f"{creator}:player": "1",
            f"{creator}:orientation": "white",
            "fen": '',
            "move": '',
            "turn": '',
        }
        
        # Convert all values to strings
        serialized_data = {k: str(v) for k, v in initial_room_data.items()}
        
        self.redis_instance.hmset(redis_key, serialized_data)
        
        return initial_room_data

    def join_room(self, room_name, username):
        if not room_name or not username:
            raise InvalidInputError("Room name and username are required")

        redis_key = f"room:{room_name}"
        if not self.room_exists(room_name):
            raise RoomNotFoundError(f"Room {room_name} does not exist")

        current_players = int(self.redis_instance.hget(redis_key, "players") or 0)
        if current_players >= 2:
            raise RoomFullError(f"Room {room_name} is full (max 2 players)")

        existing_players = self.redis_instance.hkeys(redis_key)
        for player_key in existing_players:
            if player_key.endswith(b":player"):
                existing_username = player_key.decode('utf-8').split(':')[0]
                if existing_username == username:
                    raise InvalidInputError(f"Username '{username}' is already taken in this room")

        player_num = current_players + 1
        orientation = "black" if player_num == 2 else "white"

        self.redis_instance.hset(redis_key, f"{username}:player", player_num)
        self.redis_instance.hset(redis_key, f"{username}:orientation", orientation)
        self.redis_instance.hincrby(redis_key, "players", 1)

        return self.get_room_data(room_name, username)
    
    def get_room_data(self, room_name, username):
        if not room_name or not username:
            raise InvalidInputError("Room name and username are required")

        redis_key = f"room:{room_name}"
        if not self.room_exists(room_name):
            raise RoomNotFoundError(f"Room {room_name} does not exist")

        room_data = self.redis_instance.hgetall(redis_key)
        room_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in room_data.items()}

        return {
            "room_name": room_name,
            "creator": room_data.get("creator", ""),
            "players": int(room_data.get("players", 0)),
            username: {
                "player": room_data.get(f"{username}:player", ""),
                "orientation": room_data.get(f"{username}:orientation", ""),
            },
            "fen": room_data.get("fen", ""),
            "move": self._decode_json(room_data.get("move", "")),
            "turn": room_data.get("turn", ""),
        }

    def update_fen(self, room_name, move, fen, turn):
        redis_key = f"room:{room_name}"
        self.redis_instance.hset(redis_key, "move", json.dumps(move))
        self.redis_instance.hset(redis_key, "fen", fen)
        self.redis_instance.hset(redis_key, "turn", turn)

    def reset_room(self, room_name, username):
        redis_key = f"room:{room_name}"
        player_number = int(self.redis_instance.hget(redis_key, f"{username}:player") or 0)
        
        if player_number == 0:
            raise InvalidInputError(f"Username '{username}' does not exist in room '{room_name}'")

        self.redis_instance.hdel(redis_key, f"{username}:player", f"{username}:orientation")
        
        current_players = int(self.redis_instance.hget(redis_key, "players") or 0)
        
        if current_players == 1:
            # If there was only one player, delete the room
            self.redis_instance.delete(redis_key)
        else:
            remaining_players = [key.decode('utf-8') for key in self.redis_instance.hkeys(redis_key) if key.endswith(b":player")]
            
            if player_number == 1:
                # If player 1 leaves, player 2 becomes player 1
                for key in remaining_players:
                    new_player = key.split(':')[0]
                    self.redis_instance.hset(redis_key, f"{new_player}:player", 1)
                    self.redis_instance.hset(redis_key, f"{new_player}:orientation", "white")
            
            # Update the players count
            self.redis_instance.hset(redis_key, "players", current_players - 1)
            
            # Reset game state if necessary
            self.redis_instance.hset(redis_key, "fen", '')
            self.redis_instance.hset(redis_key, "move", '')
            self.redis_instance.hset(redis_key, "turn", '')


    def _decode_json(self, value):
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return {}
        return {}