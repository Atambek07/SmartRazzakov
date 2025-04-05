from rest_framework.views import APIView
from rest_framework.response import Response
from ..application.use_cases.route_finder import RouteFinderUseCase
from ..infrastructure.repositories.django_route_repository import DjangoRouteRepository


class RouteAPIView(APIView):
    """
    API для поиска маршрутов между точками
    Пример запроса:
    GET /api/routes/?start=42.87,74.56&end=42.88,74.57&optimization=fastest
    """

    def get(self, request):
        # Валидация параметров
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        optimization = request.query_params.get('optimization', 'fastest')

        if not start or not end:
            return Response(
                {"error": "Параметры start и end обязательны"},
                status=400
            )

        try:
            # Преобразуем координаты из строки в кортеж float
            start_coords = tuple(map(float, start.split(',')))
            end_coords = tuple(map(float, end.split(',')))

            # Инициализируем зависимости
            repository = DjangoRouteRepository()
            use_case = RouteFinderUseCase(repository)

            # Выполняем основной сценарий
            route = use_case.execute(start_coords, end_coords, optimization)

            return Response({
                "route": route.number,
                "stops": route.stops,
                "estimated_time": route.estimated_time,
                "price": route.price
            })

        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        except Exception as e:
            return Response({"error": "Внутренняя ошибка сервера"}, status=500)