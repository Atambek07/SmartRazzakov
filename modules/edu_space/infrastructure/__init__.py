# modules/edu_space/infrastructure/__init__.py
from .models import (
    EducationalContentModel,
    CourseModel,
    SchoolModel,
    TestResultModel,
    UserProfileModel,
    ContentType,
    CourseLevel,
    UserRole
)

from .repositories import (
    DjangoContentRepository,
    DjangoUserRepository
)

from .integrations import (
    PaymentGatewayFactory,
    VideoServiceFactory,
    BasePaymentGateway,
    BaseVideoService,
    PaymentError,
    VideoConferenceError
)

__all__ = [
    # Models
    'EducationalContentModel',
    'CourseModel',
    'SchoolModel',
    'TestResultModel',
    'UserProfileModel',
    'ContentType',
    'CourseLevel',
    'UserRole',
    
    # Repositories
    'DjangoContentRepository',
    'DjangoUserRepository',
    
    # Integrations
    'PaymentGatewayFactory',
    'VideoServiceFactory',
    'BasePaymentGateway',
    'BaseVideoService',
    'PaymentError',
    'VideoConferenceError'
]

# Инициализация интеграций по умолчанию
default_payment_gateway = PaymentGatewayFactory.get_gateway()
default_video_service = VideoServiceFactory.get_service()