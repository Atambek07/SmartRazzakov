# modules/gov_connect/infrastructure/repositories/emergency_repo.py
from ...domain.entities import EmergencyAlert, EmergencyZone
from .models.emergency import EmergencyAlertModel, EmergencyZoneModel

class DjangoEmergencyAlertRepository:
    def save(self, alert: EmergencyAlert):
        return EmergencyAlertModel.objects.create(**alert.dict())

class DjangoEmergencyZoneRepository:
    def find_by_ids(self, zone_ids: list) -> List[EmergencyZone]:
        return [
            EmergencyZone(**zone.__dict__)
            for zone in EmergencyZoneModel.objects.filter(id__in=zone_ids)
        ]