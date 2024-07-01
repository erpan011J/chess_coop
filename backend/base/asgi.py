import os
import django
django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chess.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chess.routing.websocket_urlpatterns
        )
    ),
})
