from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, ContentViewSet, TutorViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Инициализация роутера API
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'content', ContentViewSet, basename='content')
router.register(r'tutors', TutorViewSet, basename='tutor')

urlpatterns = [
    # API endpoints
    path('', include(router.urls)),
    
    # Аутентификация
    path('auth/jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    
    # Детализация курсов
    path('courses/<uuid:pk>/sessions/', 
         include([
             path('schedule/', CourseViewSet.as_view({'post': 'schedule_session'}), 
                  name='course-schedule-session'),
             path('enroll/', CourseViewSet.as_view({'post': 'enroll'}), 
                  name='course-enroll')
         ])),
    
    # Работа с контентом
    path('content/<uuid:pk>/', 
         include([
             path('publish/', ContentViewSet.as_view({'post': 'publish'}), 
                  name='content-publish'),
             path('upload/', ContentViewSet.as_view({'post': 'upload_file'}), 
                  name='content-upload')
         ])),
    
    # Функционал репетиторов
    path('tutors/<uuid:pk>/', 
         include([
             path('schedule/', TutorViewSet.as_view({'get': 'schedule'}), 
                  name='tutor-schedule'),
             path('book/', TutorViewSet.as_view({'post': 'book_session'}), 
                  name='tutor-book')
         ])),
]

app_name = 'edu_space_api'