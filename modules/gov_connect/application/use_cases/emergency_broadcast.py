# modules/gov_connect/application/use_cases/emergency_broadcast.py
from ...domain.services import EmergencyService
from ...infrastructure.repositories import (
    DjangoEmergencyAlertRepository,
    DjangoEmergencyZoneRepository
)
from ...infrastructure.integrations.emergency_channels import (
    SMSChannel,
    SirenControlChannel
)

class EmergencyBroadcastUseCase:
    def __init__(self):
        self.repo = DjangoEmergencyAlertRepository()
        self.zone_repo = DjangoEmergencyZoneRepository()
        self.channels = {
            "sms": SMSChannel(),
            "sirens": SirenControlChannel()
        }
        self.service = EmergencyService(
            self.repo,
            self.zone_repo,
            self.channels
        )

    def execute(self, alert_data: dict):
        alert = EmergencyAlert(**alert_data)
        return self.service.broadcast_alert(alert)