from city_routes.domain.services import NotificationService
from city_routes.domain.entities import UserPreference


class UserNotificationUseCase:
    def __init__(self, notification_service: NotificationService, user_repository):
        self.service = notification_service
        self.user_repo = user_repository

    async def send_route_update(self, user_id: str, route_id: str, message: str):
        user = await self.user_repo.get_by_id(user_id)
        prefs = UserPreference(**user.notification_prefs)

        if prefs.route_updates:
            await self.service.send(
                recipient=user.contact_info,
                message_type="route_update",
                content={
                    "route_id": route_id,
                    "message": message
                },
                priority=prefs.priority_level
            )

    async def broadcast_traffic_alert(self, alert_id: str):
        alert = await self.traffic_repo.get_by_id(alert_id)
        affected_users = await self.user_repo.get_users_in_radius(
            alert.location, alert.radius
        )

        for user in affected_users:
            await self.send_route_update(
                user.id,
                alert_id,
                f"Traffic alert: {alert.description}"
            )