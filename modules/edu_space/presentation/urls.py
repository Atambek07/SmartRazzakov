from django.urls import path
from .presentation.views import (
    CourseListView,
    CourseDetailView,
    ClassroomScheduleView,
    TutorSearchView
)

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('classrooms/schedule/', ClassroomScheduleView.as_view(), name='schedule-class'),
    path('tutors/', TutorSearchView.as_view(), name='tutor-search'),
]