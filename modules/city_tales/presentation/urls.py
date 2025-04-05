from django.urls import path
from .presentation.views import StoryCreateView, StoryDetailView

urlpatterns = [
    path('stories/', StoryCreateView.as_view(), name='create-story'),
    path('stories/<int:pk>/', StoryDetailView.as_view(), name='story-detail'),
    path('qr/<int:story_id>/', QRCodeView.as_view(), name='qr-code'),
]

