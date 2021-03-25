# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/trim/', consumers.TrimConsumer.as_asgi()),
]