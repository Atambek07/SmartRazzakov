from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    RouteListView,
    RouteDetailView,
    RouteCreateView,
    RouteUpdateView,
    RouteDeleteView,
    TrafficAlertView,
    TrafficAnalysisView,
    TransportListView,
    TransportDetailView,
    TransportMapView,
    TransportDataView
)

urlpatterns = [
    # Маршруты
    path('routes/', include([
        path('', RouteListView.as_view(), name='route-list'),
        path('create/', RouteCreateView.as_view(), name='route-create'),
        path('<uuid:pk>/', include([
            path('', RouteDetailView.as_view(), name='route-detail'),
            path('edit/', RouteUpdateView.as_view(), name='route-update'),
            path('delete/', RouteDeleteView.as_view(), name='route-delete'),
        ])),
    ])),
    
    # Трафик
    path('traffic/', include([
        path('alerts/', TrafficAlertView.as_view(), name='traffic-alerts'),
        path('analysis/', TrafficAnalysisView.as_view(), name='traffic-analysis'),
    ])),
    
    # Транспорт
    path('transport/', include([
        path('', TransportListView.as_view(), name='transport-list'),
        path('map/', TransportMapView.as_view(), name='transport-map'),
        path('data/', TransportDataView.as_view(), name='transport-data'),
        path('<str:vehicle_id>/', TransportDetailView.as_view(), name='transport-detail'),
    ])),
    
    # Главная страница
    path('', RouteListView.as_view(), name='home'),
]

# Добавляем статические файлы в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Документация API (drf-yasg)
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    
    schema_view = get_schema_view(
        openapi.Info(
            title="Smart Razakov API",
            default_version='v1',
            description="API для цифровой платформы города Раззаков",
            contact=openapi.Contact(email="tech@razakov.gov.kz"),
            license=openapi.License(name="City Government License"),
        ),
        public=True,
    )
    
    urlpatterns += [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]