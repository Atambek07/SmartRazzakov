from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point
from uuid import UUID
from typing import Optional
from ..serializers import (
    RouteInputSerializer,
    RouteOutputSerializer,
    RouteUpdateSerializer
)
from infrastructure.repositories import DjangoRouteRepository
from domain.exceptions import RouteNotFoundError, InvalidRouteError

class RouteListView(APIView):
    """API для работы с коллекцией маршрутов"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DjangoRouteRepository()

    def post(self, request):
        """Создание нового маршрута"""
        serializer = RouteInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            route = self.repo.save(serializer.validated_data)
            output = RouteOutputSerializer(route)
            return Response(output.data, status=status.HTTP_201_CREATED)
        except InvalidRouteError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """Поиск маршрутов по параметрам"""
        params = {
            'start_point': request.query_params.get('start_point'),
            'end_point': request.query_params.get('end_point'),
            'transport_type': request.query_params.get('transport_type'),
            'max_distance': request.query_params.get('max_distance')
        }
        
        # Преобразование параметров
        if params['start_point']:
            params['start_point'] = [float(x) for x in params['start_point'].split(',')]
        
        routes = self.repo.find_by_criteria(**params)
        serializer = RouteOutputSerializer(routes, many=True)
        return Response(serializer.data)

class RouteDetailView(APIView):
    """API для работы с конкретным маршрутом"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = DjangoRouteRepository()

    def get(self, request, route_id: UUID):
        """Получение деталей маршрута"""
        try:
            route = self.repo.get_by_id(route_id)
            serializer = RouteOutputSerializer(route)
            return Response(serializer.data)
        except RouteNotFoundError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, route_id: UUID):
        """Обновление маршрута"""
        serializer = RouteUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            updated = self.repo.update(route_id, serializer.validated_data)
            output = RouteOutputSerializer(updated)
            return Response(output.data)
        except RouteNotFoundError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except InvalidRouteError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, route_id: UUID):
        """Удаление маршрута"""
        try:
            self.repo.delete(route_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except RouteNotFoundError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)