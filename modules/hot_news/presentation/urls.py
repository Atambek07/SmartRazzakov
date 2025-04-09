from django.urls import path
from .views import (
    NewsAPIView,
    NewsDetailAPIView,
    SubscriptionAPIView,
    EmergencyAPIView
)

urlpatterns = [
    # News endpoints
    path(
        'news/',
        NewsAPIView.as_view(),
        name='news-list'
    ),
    path(
        'news/<uuid:article_id>/',
        NewsDetailAPIView.as_view(),
        name='news-detail'
    ),
    
    # Subscription management
    path(
        'subscriptions/',
        SubscriptionAPIView.as_view(),
        name='subscription-management'
    ),
    
    # Emergency alerts
    path(
        'emergency/alerts/',
        EmergencyAPIView.as_view(),
        name='emergency-alerts'
    ),
]