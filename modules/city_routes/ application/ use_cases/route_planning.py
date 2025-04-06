from typing import List
from city_routes.domain.entities import RoutePlan
from city_routes.domain.services import RouteAnalyzer


class RoutePlanningUseCase:
    def __init__(self, analyzer: RouteAnalyzer):
        self.analyzer = analyzer

    async def create_daily_plan(self, user_id: str, destinations: List[tuple]) -> RoutePlan:
        analysis = await self.analyzer.analyze_destinations(destinations)
        return RoutePlan(
            user_id=user_id,
            optimized_routes=analysis.optimal_order,
            estimated_total_time=analysis.total_duration,
            transport_mix=analysis.recommended_transport
        )

    async def adjust_plan_for_traffic(self, plan_id: str) -> RoutePlan:
        current_plan = await self.plan_repo.get_by_id(plan_id)
        traffic_data = await self.traffic_service.get_current()

        adjusted = await self.analyzer.adjust_for_traffic(
            original_plan=current_plan,
            traffic_conditions=traffic_data
        )

        return await self.plan_repo.update(plan_id, adjusted)