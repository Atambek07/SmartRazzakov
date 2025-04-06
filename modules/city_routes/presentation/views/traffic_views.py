from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import (
    TrafficAlertSerializer,
    TrafficAnalysisSerializer
)
from infrastructure.repositories import DjangoTrafficRepository
from domain.exceptions import TrafficAlertConflictError

class TrafficAlertView(APIView):
    """API для работы с оповещениями о трафике"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DjangoTrafficRepository()

    def post(self, request):
        """Создание нового оповещения"""
        serializer = TrafficAlertSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            alert = self.repo.create(serializer.validated_data)
            return Response(
                TrafficAlertSerializer(alert).data,
                status=status.HTTP_201_CREATED
            )
        except TrafficAlertConflictError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_409_CONFLICT
            )

    def get(self, request):
        """Получение активных оповещений"""
        alerts = self.repo.get_active_alerts()
        serializer = TrafficAlertSerializer(alerts, many=True)
        return Response(serializer.data)

class TrafficAnalysisView(APIView):
    """API для анализа трафика"""
    
    def get(self, request):
        """Получение текущей аналитики трафика"""
        analysis = self._get_traffic_analysis()
        serializer = TrafficAnalysisSerializer(analysis)
        return Response(serializer.data)

    def _get_traffic_analysis(self):
        """Логика получения данных о трафике"""
        # Здесь может быть интеграция с внешними сервисами
        return {
            'congestion_level': 0.7,
            'hotspots': [],
            'updated_at': '2023-01-01T12:00:00Z'
        }