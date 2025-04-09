# modules/gov_connect/infrastructure/__init__.py
"""
Инфраструктурный слой модуля GovConnect

Содержит все реализации, специфичные для внешнего мира:
- Модели данных (Django ORM)
- Репозитории для работы с хранилищами
- Интеграции с внешними сервисами
"""

from .models import (
    Complaint,
    ComplaintPhoto,
    GovernmentService,
    ServiceCategory
)
from .repositories import (
    DjangoComplaintRepository,
    DjangoServiceRepository
)
from .integrations import (
    DocumentParser,
    PDFParser,
    ImageOCRParser,
    GISAdapter,
    GoogleMapsGIS,
    OpenStreetMapGIS,
    NotificationService,
    TwilioSMSNotifier,
    SendGridEmailNotifier,
    FirebasePushNotifier
)

__all__ = [
    # Models
    'Complaint',
    'ComplaintPhoto',
    'GovernmentService',
    'ServiceCategory',
    
    # Repositories
    'DjangoComplaintRepository',
    'DjangoServiceRepository',
    
    # Integrations
    'DocumentParser',
    'PDFParser',
    'ImageOCRParser',
    'GISAdapter',
    'GoogleMapsGIS',
    'OpenStreetMapGIS',
    'NotificationService',
    'TwilioSMSNotifier',
    'SendGridEmailNotifier',
    'FirebasePushNotifier'
]

def initialize_infrastructure(config: dict):
    """Инициализация инфраструктурных компонентов"""
    from .integrations import (
        GoogleMapsGIS,
        TwilioSMSNotifier,
        SendGridEmailNotifier
    )
    
    services = {
        'gis_service': GoogleMapsGIS(api_key=config['GOOGLE_MAPS_API_KEY']),
        'sms_notifier': TwilioSMSNotifier(
            account_sid=config['TWILIO_SID'],
            auth_token=config['TWILIO_TOKEN'],
            from_number=config['TWILIO_NUMBER']
        ),
        'email_notifier': SendGridEmailNotifier(
            api_key=config['SENDGRID_API_KEY']
        )
    }
    
    return services