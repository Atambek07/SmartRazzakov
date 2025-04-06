from abc import ABC, abstractmethod
from typing import Dict, List
from ..entities import UserPreferences
from ..exceptions import NotificationFailedError

class SMSService(ABC):
    """Абстрактный сервис отправки SMS-уведомлений"""
    
    @abstractmethod
    async def send(
        self,
        phone_number: str,
        message: str,
        user_prefs: Optional[UserPreferences] = None
    ) -> bool:
        """
        Отправляет SMS сообщение
        Args:
            phone_number: номер телефона получателя
            message: текст сообщения
            user_prefs: предпочтения пользователя для персонализации
        Returns:
            True если отправка успешна
        Raises:
            NotificationFailedError: если отправка не удалась
        """
        pass

    @abstractmethod
    async def broadcast(
        self,
        recipients: List[str],
        message_template: str,
        context: Dict
    ) -> int:
        """
        Массовая рассылка сообщений
        Args:
            recipients: список номеров телефонов
            message_template: шаблон сообщения (например, "Маршрут {route_id} изменен")
            context: данные для подстановки в шаблон
        Returns:
            Количество успешно отправленных сообщений
        """
        pass