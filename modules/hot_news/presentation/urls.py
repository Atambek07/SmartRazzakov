from django.urls import path
from .presentation.views import (
    NewsAPI,
    NewsDetailAPI,
    EmergencyAlertAPI,
    SubscriptionAPI
)

urlpatterns = [
    path('news/', NewsAPI.as_view(), name='news-list'),
    path('news/<int:pk>/', NewsDetailAPI.as_view(), name='news-detail'),
    path('alerts/emergency/', EmergencyAlertAPI.as_view(), name='emergency-alert'),
    path('subscriptions/', SubscriptionAPI.as_view(), name='news-subscriptions'),
]