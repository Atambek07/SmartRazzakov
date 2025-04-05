from django.urls import path
from .presentation.views import (
    CommunityAPI,
    CommunityDetailAPI,
    CommunityChatAPI
)
from .presentation.consumers import CommunityChatConsumer

websocket_urlpatterns = [
    path('ws/communities/<int:community_id>/', CommunityChatConsumer.as_asgi()),
]

urlpatterns = [
    path('communities/', CommunityAPI.as_view(), name='community-list'),
    path('communities/<int:pk>/', CommunityDetailAPI.as_view(), name='community-detail'),
    path('communities/<int:pk>/chat/', CommunityChatAPI.as_view(), name='community-chat'),
]