# modules/gov_connect/infrastructure/integrations/__init__.py
"""
Интеграции с внешними сервисами для GovConnect

Содержит:
- Парсер документов
- GIS-интеграцию
- Систему уведомлений
"""

from .document_parser import DocumentParser, PDFParser, ImageOCRParser
from .gis_integration import GISAdapter, GoogleMapsGIS, OpenStreetMapGIS
from .notification_system import (
    NotificationService,
    TwilioSMSNotifier,
    SendGridEmailNotifier,
    FirebasePushNotifier
)

__all__ = [
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