# modules/community_hub/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .presentation.views import (
    CommunityViewSet,
    EventViewSet,
    ModerationViewSet
)

router = DefaultRouter()
router.register(r'communities', CommunityViewSet, basename='community')
router.register(
    r'communities/(?P<community_id>[^/.]+)/events',
    EventViewSet,
    basename='community-event'
)
router.register(
    r'communities/(?P<community_id>[^/.]+)/moderation',
    ModerationViewSet,
    basename='community-moderation'
)

websocket_urlpatterns = [
    path(
        'ws/communities/<uuid:community_id>/chat/',
        ChatConsumer.as_asgi()
    ),
]

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/ws/', include(websocket_urlpatterns)),
]