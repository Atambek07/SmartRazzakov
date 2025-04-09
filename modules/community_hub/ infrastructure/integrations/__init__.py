# modules/community_hub/infrastructure/integrations/__init__.py
from typing import Type, Dict, Any, Optional
from abc import ABC, abstractmethod
import logging
from uuid import UUID
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class IntegrationError(Exception):
    """Базовое исключение для интеграционных ошибок"""

    def __init__(self, service: str, message: str, details: Optional[Dict] = None):
        self.service = service
        self.message = message
        self.details = details or {}
        super().__init__(f"{service} error: {message}")


class ServiceType(Enum):
    """Типы внешних сервисов"""
    EMAIL = "email"
    SMS = "sms"
    PAYMENT = "payment"
    NOTIFICATION = "notification"
    SEARCH = "search"
    STORAGE = "storage"


@dataclass
class IntegrationConfig:
    """Конфигурация для интеграций"""
    service_type: ServiceType
    endpoint: str
    api_key: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3
    circuit_breaker: bool = True


class BaseIntegrationClient(ABC):
    """Абстрактный базовый клиент для интеграций"""

    def __init__(self, config: IntegrationConfig):
        self.config = config
        self._is_connected = False

    @abstractmethod
    async def connect(self) -> bool:
        """Установка соединения с сервисом"""
        pass

    @abstractmethod
    async def disconnect(self) -> bool:
        """Закрытие соединения"""
        pass

    @property
    def is_connected(self) -> bool:
        """Статус подключения"""
        return self._is_connected

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Проверка работоспособности сервиса"""
        pass


class EmailServiceClient(BaseIntegrationClient):
    """Абстракция для email сервиса"""

    @abstractmethod
    async def send_email(
            self,
            to: str,
            subject: str,
            body: str,
            template_id: Optional[str] = None,
            context: Optional[Dict] = None
    ) -> bool:
        pass


class SMSServiceClient(BaseIntegrationClient):
    """Абстракция для SMS сервиса"""

    @abstractmethod
    async def send_sms(
            self,
            phone: str,
            message: str,
            sender: Optional[str] = None
    ) -> bool:
        pass


class PaymentServiceClient(BaseIntegrationClient):
    """Абстракция для платежного сервиса"""

    @abstractmethod
    async def create_payment(
            self,
            amount: float,
            currency: str,
            user_id: UUID,
            description: str
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def refund_payment(self, payment_id: str) -> bool:
        pass


class StorageServiceClient(BaseIntegrationClient):
    """Абстракция для сервиса хранения файлов"""

    @abstractmethod
    async def upload_file(
            self,
            file_path: str,
            bucket: str,
            object_name: Optional[str] = None,
            metadata: Optional[Dict] = None
    ) -> str:
        pass

    @abstractmethod
    async def generate_presigned_url(
            self,
            object_name: str,
            bucket: str,
            expiration: int = 3600
    ) -> str:
        pass


# Реэкспорт основных компонентов
__all__ = [
    'IntegrationError',
    'ServiceType',
    'IntegrationConfig',
    'BaseIntegrationClient',
    'EmailServiceClient',
    'SMSServiceClient',
    'PaymentServiceClient',
    'StorageServiceClient'
]


# Фабрика интеграционных клиентов
def create_integration_client(
        service_type: ServiceType,
        config: IntegrationConfig
) -> BaseIntegrationClient:
    """Фабрика для создания клиентов интеграций"""
    # В реальной реализации здесь будет логика создания конкретных клиентов
    # Например, для ServiceType.EMAIL может возвращаться SendGridClient или MailgunClient
    raise NotImplementedError("Integration client factory not implemented")