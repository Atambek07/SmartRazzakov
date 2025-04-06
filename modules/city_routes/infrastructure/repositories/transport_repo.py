from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from domain.entities import TransportVehicle
from domain.exceptions import TransportNotFoundError

class TransportRepository(ABC):
    """Абстрактный репозиторий для работы с транспортом"""
    
    @abstractmethod
    async def get_by_id(self, vehicle_id: str) -> TransportVehicle:
        pass

    @abstractmethod
    async def save(self, vehicle: TransportVehicle) -> TransportVehicle:
        pass

    @abstractmethod
    async def find_nearby(
        self,
        location: tuple[float, float],
        radius_km: float,
        transport_type: Optional[str] = None
    ) -> List[TransportVehicle]:
        pass

class DjangoTransportRepository(TransportRepository):
    """Реализация репозитория транспорта на Django ORM"""
    
    def __init__(self):
        from ..models import TransportVehicleModel
        self.model = TransportVehicleModel

    async def get_by_id(self, vehicle_id: str) -> TransportVehicle:
        try:
            vehicle = await self.model.objects.aget(pk=vehicle_id)
            return self._to_domain_entity(vehicle)
        except self.model.DoesNotExist as e:
            raise TransportNotFoundError(vehicle_id) from e

    async def save(self, vehicle: TransportVehicle) -> TransportVehicle:
        from django.contrib.gis.geos import Point
        from ..models import TransportTypeModel

        transport_type = await TransportTypeModel.objects.aget(code=vehicle.vehicle_type.value)
        
        defaults = {
            'type': transport_type,
            'current_location': Point(vehicle.current_location[1], vehicle.current_location[0]),
            'capacity': vehicle.capacity,
            'is_active': vehicle.available,
            'license_plate': getattr(vehicle, 'license_plate', ''),
            'properties': getattr(vehicle, 'properties', {})
        }

        vehicle_model, _ = await self.model.objects.aupdate_or_create(
            id=vehicle.id,
            defaults=defaults
        )
        return self._to_domain_entity(vehicle_model)

    async def find_nearby(
        self,
        location: tuple[float, float],
        radius_km: float,
        transport_type: Optional[str] = None
    ) -> List[TransportVehicle]:
        from django.contrib.gis.geos import Point
        from django.contrib.gis.measure import D
        from ..models import TransportTypeModel

        point = Point(location[1], location[0])
        query = self.model.objects.filter(
            current_location__distance_lte=(point, D(km=radius_km)),
            is_active=True
        )

        if transport_type:
            transport_type_obj = await TransportTypeModel.objects.aget(code=transport_type)
            query = query.filter(type=transport_type_obj)

        vehicles = []
        async for vehicle in query.select_related('type'):
            vehicles.append(self._to_domain_entity(vehicle))
        return vehicles

    def _to_domain_entity(self, vehicle) -> TransportVehicle:
        return TransportVehicle(
            id=vehicle.id,
            vehicle_type=vehicle.type.code,
            current_location=(vehicle.current_location.y, vehicle.current_location.x),
            capacity=vehicle.capacity,
            available=vehicle.is_active,
            last_maintenance=getattr(vehicle, 'last_maintenance', None)
        )