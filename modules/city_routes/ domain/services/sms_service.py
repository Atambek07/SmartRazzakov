from abc import ABC, abstractmethod


class SMSService(ABC):
    """Абстрактный сервис для отправки SMS."""

    @abstractmethod
    def send_sms(self, phone: str, message: str) -> bool:
        """
        Отправляет SMS пользователю.

        :param phone: Номер телефона (формат: "+996XXXXXXXXX").
        :param message: Текст сообщения.
        :return: True, если отправка успешна.
        """
        pass

    @abstractmethod
    def format_route_message(self, route) -> str:
        """Форматирует данные маршрута для SMS."""
        pass