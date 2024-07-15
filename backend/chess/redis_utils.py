import redis
import json
import logging

logger = logging.getLogger(__name__)

class RedisHandler:
    def __init__(self):
        self.redis_instance = redis.StrictRedis(host='redis', port=6379, db=0)

    def room_exists(self, room_name):
        redis_key = f"room:{room_name}"
        return self.redis_instance.exists(redis_key)

    def create_room(self, room_name, creator):
        redis_key = f"room:{room_name}"
        self.redis_instance.hset(redis_key, "room_name", room_name)
        self.redis_instance.hset(redis_key, "creator", creator)
        self.redis_instance.hset(redis_key, "players", 1)
        self.redis_instance.hset(redis_key, f"{creator}:player", 1)
        self.redis_instance.hset(redis_key, f"{creator}:orientation", "white")
        self.redis_instance.hset(redis_key, "fen", '')
        self.redis_instance.hset(redis_key, "move", '')
        self.redis_instance.hset(redis_key, "turn", '')

        initial_room_data = {
            "room_name": room_name,
            "creator": creator,
            "players": 1,
            creator: {
                "player": 1,
                "orientation": "white",
            },
            "fen": '',
            "move": '',
            "turn": '',
        }
        return initial_room_data

    def join_room(self, room_name, username):
        redis_key = f"room:{room_name}"
        current_players = int(self.redis_instance.hget(redis_key, "players") or 0)

        if current_players >= 2:
            return {'error': 'Room is full (max 2 players)'}

        player_num = current_players + 1
        orientation = "black" if player_num == 2 else "white"

        self.redis_instance.hset(redis_key, f"{username}:player", player_num)
        self.redis_instance.hset(redis_key, f"{username}:orientation", orientation)
        self.redis_instance.hset(redis_key, "players", player_num)

        room_data = {
            "room_name": room_name,
            "creator": self.redis_instance.hget(redis_key, "creator").decode('utf-8'),
            "players": player_num,
            username: {
                "player": player_num,
                "orientation": orientation,
            },
            "fen": self.redis_instance.hget(redis_key, "fen").decode('utf-8') if self.redis_instance.hexists(redis_key, "fen") else '',
            "move": self._decode_json(self.redis_instance.hget(redis_key, "move")),
            "turn": self.redis_instance.hget(redis_key, "turn").decode('utf-8') if self.redis_instance.hexists(redis_key, "turn") else '',
        }
        return room_data

    def get_room_data(self, room_name , username):
        redis_key = f"room:{room_name}"
        creator = self.redis_instance.hget(redis_key, "creator").decode('utf-8')
        player_number = self.redis_instance.hget(redis_key, f"{username}:player").decode('utf-8')
        orientation = self.redis_instance.hget(redis_key, f"{username}:orientation").decode('utf-8')
        
        room_data = {
            "room_name": room_name,
            "creator": creator,
            "players": int(self.redis_instance.hget(redis_key, "players") or 0),
            username: {
                "player": player_number,
                "orientation": orientation,
            },
            "fen": self.redis_instance.hget(redis_key, "fen").decode('utf-8') if self.redis_instance.hexists(redis_key, "fen") else '',
            "move": self._decode_json(self.redis_instance.hget(redis_key, "move")),
            "turn": self.redis_instance.hget(redis_key, "turn").decode('utf-8') if self.redis_instance.hexists(redis_key, "turn") else '',
        }
        
        return room_data

    def update_fen(self, room_name, move, fen, turn):
        redis_key = f"room:{room_name}"
        self.redis_instance.hset(redis_key, "move", json.dumps(move))
        self.redis_instance.hset(redis_key, "fen", fen)
        self.redis_instance.hset(redis_key, "turn", turn)

    
    def reset_room(self, room_name, username):
        redis_key = f"room:{room_name}"
        player_number = int(self.redis_instance.hget(redis_key, f"{username}:player").decode('utf-8'))
        if player_number == 1:
            self.redis_instance.delete(redis_key)
        elif player_number == 2:
            self.redis_instance.hdel(redis_key, username)
            self.redis_instance.hset(redis_key, "players", 1)
            self.redis_instance.hset(redis_key, "fen", '')
            self.redis_instance.hset(redis_key, "move", '')
            self.redis_instance.hset(redis_key, "turn", '') 
        
    def _decode_json(self, value):
        if value and isinstance(value, bytes):
            try:
                return json.loads(value.decode('utf-8'))
            except json.JSONDecodeError:
                return {}
        return {}
