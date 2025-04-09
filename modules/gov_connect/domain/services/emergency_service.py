# modules/gov_connect/domain/services/emergency_service.py
from ...domain.entities import EmergencyAlert, EmergencyZone
from ...domain.exceptions import EmergencyServiceError
from typing import List

class EmergencyService:
    def __init__(self, alert_repo, zone_repo, notification_channels):
        self.alert_repo = alert_repo
        self.zone_repo = zone_repo
        self.channels = notification_channels

    def broadcast_alert(self, alert: EmergencyAlert) -> dict:
        if not alert.zones:
            raise EmergencyServiceError("No zones specified")
        
        affected_zones = self.zone_repo.find_by_ids(alert.zones)
        if not affected_zones:
            raise EmergencyServiceError("Invalid zones")

        results = {}
        for channel in alert.channels:
            if channel not in self.channels:
                continue
            try:
                self.channels[channel].send(alert, affected_zones)
                results[channel] = "success"
            except Exception as e:
                results[channel] = str(e)
        
        return results