from django.urls import path
from .presentation.views import (
    PublicReviewAPI,
    BusinessRatingAPI,
    ModerationAPI
)

urlpatterns = [
    path('reviews/', PublicReviewAPI.as_view(), name='submit-review'),
    path('reviews/<str:target_id>/', PublicReviewAPI.as_view(), name='get-reviews'),
    path('ratings/<str:target_id>/', BusinessRatingAPI.as_view(), name='get-rating'),
    path('moderate/reviews/', ModerationAPI.as_view(), name='moderate-reviews'),
]