from rest_framework.views import APIView
from rest_framework.response import Response
from ..application.use_cases.route_planning import PlanRouteUseCase
from ..domain.services import RoutePlanner
from ..infrastructure.integrations import OSMMapProvider

class PublicTransportAPI(APIView):
    def post(self, request):
        serializer = RoutePlanSerializer(data=request.data)
        if serializer.is_valid():
            planner = RoutePlanner(OSMMapProvider())
            use_case = PlanRouteUseCase(planner)
            result = use_case.execute(serializer.validated_data)
            return Response(result)
        return Response(serializer.errors, status=400)