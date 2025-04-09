# modules/health_connect/infrastructure/repositories/__init__.py
from .medical_repo import *
from .user_repo import *

__all__ = [
    'MedicalRepository',
    'UserRepository'
]