from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from .redis_utils import RedisHandler
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

redis_instance = RedisHandler()

class RoomViewSet(viewsets.ViewSet):
    def create(self, request):
        room_name = request.data.get('name')
        username = request.data.get('username')
        if not room_name:
            return Response({'error': 'Room Name is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if room name already exists in Redis
        if redis_instance.room_exists(room_name):
            return Response({'error': 'Room Name already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Set initial room data in Redis
        initial_room_data = redis_instance.create_room(room_name, username)

        return Response(initial_room_data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        room_name = pk
        username = request.data.get('username')

        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Join the room and get updated room data
        room_data = redis_instance.join_room(room_name, username)

        return Response(room_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def initial_data(self, request, pk=None):
        room_name = pk
        username = request.data.get('username')
        
        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch initial room data from Redis
        room_data = redis_instance.get_room_data(room_name, username)
        
        return Response(room_data, status=status.HTTP_200_OK)
