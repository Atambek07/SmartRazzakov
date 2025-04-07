from django.urls import path
from . import views
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path(
        'tales/scan/',
        views.TaleContentView.as_view(),
        name='tale-content'
    ),
    path(
        'user/preferences/',
        views.UserPreferenceView.as_view(),
        name='user-preferences'
    ),
    path(
        'schema/',
        SpectacularAPIView.as_view(),
        name='api-schema'
    ),
]