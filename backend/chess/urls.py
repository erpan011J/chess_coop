from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')  # Provide 'basename' explicitly

urlpatterns = [
    path('', include(router.urls)),
    # Other paths if any
]
