from django.urls import re_path
from .consumers import PedidoConsumer

websocket_urlpatterns = [
    re_path(r'ws/notifications/', PedidoConsumer.as_asgi()),
]