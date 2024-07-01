from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import redis

redis_instance = redis.StrictRedis(host='redis', port=6379, db=0)

class RoomViewSet(viewsets.ViewSet):
    def create(self, request):
        room_name = request.data.get('name')
        username = request.data.get('username')

        if not room_name:
            return Response({'error': 'Room Name is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if room name already exists in Redis
        redis_key = f"room:{room_name}"
        if redis_instance.exists(redis_key):
            return Response({'error': 'Room Name already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Set room data in Redis with creator and initial player
        redis_instance.hset(redis_key, "creator", username)
        redis_instance.hset(redis_key, "players", 1)  # Set initial player count

        return Response({'room_name': room_name, 'username': username}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        room_name = pk
        username = request.data.get('username')

        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if room exists in Redis and if it already has 2 players
        redis_key = f"room:{room_name}"
        if not redis_instance.exists(redis_key):
            return Response({'error': 'Room does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        current_players = int(redis_instance.hget(redis_key, "players") or 0)
        if current_players >= 2:
            return Response({'error': 'Room is full (max 2 players)'}, status=status.HTTP_400_BAD_REQUEST)

        # Set player data in Redis and increment player count
        redis_instance.hset(redis_key, f"player:{current_players + 1}", username)
        redis_instance.hset(redis_key, "players", current_players + 1)

        return Response({'room_name': room_name, 'username': username}, status=status.HTTP_200_OK)
