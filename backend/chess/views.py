# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .redis_utils import RedisHandler
from .custom_exceptions import RoomError, RoomNotFoundError, RoomFullError, InvalidInputError
import logging

logger = logging.getLogger(__name__)

class RoomViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redis_handler = RedisHandler()

    def create(self, request):
        try:
            room_name = request.data.get('name')
            username = request.data.get('username')
            
            if self.redis_handler.room_exists(room_name):
                return Response({'error': 'Room Name already exists'}, status=status.HTTP_400_BAD_REQUEST)

            initial_room_data = self.redis_handler.create_room(room_name, username)
            return Response(initial_room_data, status=status.HTTP_201_CREATED)
        except InvalidInputError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating room: {str(e)}")
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        try:
            room_name = pk
            username = request.data.get('username')
            room_data = self.redis_handler.join_room(room_name, username)
            return Response(room_data, status=status.HTTP_200_OK)
        except (RoomNotFoundError, RoomFullError, InvalidInputError) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error joining room: {str(e)}")
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def initial_data(self, request, pk=None):
        try:
            room_name = pk
            username = request.data.get('username')
            room_data = self.redis_handler.get_room_data(room_name, username)
            return Response(room_data, status=status.HTTP_200_OK)
        except (RoomNotFoundError, InvalidInputError) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error fetching initial data: {str(e)}")
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)