# modules/feedback/presentation/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/<int:review_id>/votes/', ReviewVoteView.as_view(), name='review-vote'),
    
    path('ratings/<str:module>/<str:content_type>/<int:object_id>/', 
         RatingSummaryView.as_view(), name='rating-summary'),
    
    path('moderation/queue/', ModerationQueueView.as_view(), name='moderation-queue'),
    path('moderation/<int:review_id>/', 
         ModerationActionView.as_view(), name='moderation-action'),
]