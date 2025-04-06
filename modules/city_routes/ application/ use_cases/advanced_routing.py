from typing import List
from city_routes.domain.entities import Route
from city_routes.application.dto.route_dto import RouteUpdateDTO


class AdvancedRoutingUseCase:
    def __init__(self, route_optimizer, repository):
        self.optimizer = route_optimizer
        self.repository = repository

    async def optimize_route(self, route_id: str, update_data: RouteUpdateDTO) -> Route:
        route = await self.repository.get_by_id(route_id)

        optimized = await self.optimizer.recalculate(
            existing_route=route,
            avoid_areas=update_data.avoid_areas,
            priority=update_data.priority,
            new_transport=update_data.new_transport
        )

        return await self.repository.update(route_id, optimized)

    async def find_alternative_routes(self, route_id: str, count: int = 3) -> List[Route]:
        base_route = await self.repository.get_by_id(route_id)
        return await self.optimizer.find_alternatives(
            base_route=base_route,
            max_alternatives=count
        )