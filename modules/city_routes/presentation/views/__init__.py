from .public_api import router as fastapi_router
from .route_views import RouteListView, RouteDetailView
from .traffic_views import TrafficAlertView, TrafficAnalysisView

__all__ = [
    'fastapi_router',
    'RouteListView',
    'RouteDetailView',
    'TrafficAlertView',
    'TrafficAnalysisView'
]


def admin_api():
    return None