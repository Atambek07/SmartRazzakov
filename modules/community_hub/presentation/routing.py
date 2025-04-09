from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(
        r'ws/community/(?P<community_id>[0-9a-f-]+)/chat/$',
        ChatConsumer.as_asgi()
    ),
]