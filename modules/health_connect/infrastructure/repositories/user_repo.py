# modules/health_connect/infrastructure/repositories/user_repo.py
from django.db import transaction
from typing import List, Optional
from ..models.users import PatientProfile, HealthcareProviderProfile
from ...domain.entities import HealthcareProvider
from ...domain.exceptions import UserNotFound
from core.utils.logging import LoggingService

class UserRepository:
    def __init__(self, logger: LoggingService):
        self.logger = logger

    @transaction.atomic
    def save_patient(self, patient_data: dict) -> PatientProfile:
        try:
            patient, created = PatientProfile.objects.update_or_create(
                national_id=patient_data['national_id'],
                defaults=patient_data
            )
            return patient
        except Exception as e:
            self.logger.error(f"Error saving patient: {str(e)}")
            raise

    @transaction.atomic
    def save_provider(self, provider_data: dict) -> HealthcareProviderProfile:
        try:
            provider, created = HealthcareProviderProfile.objects.update_or_create(
                license_number=provider_data['license_number'],
                defaults=provider_data
            )
            return provider
        except Exception as e:
            self.logger.error(f"Error saving provider: {str(e)}")
            raise

    def get_provider(self, provider_id: str) -> HealthcareProvider:
        try:
            model = HealthcareProviderProfile.objects.get(id=provider_id)
            return self._model_to_entity(model)
        except HealthcareProviderProfile.DoesNotExist:
            raise UserNotFound(f"Provider {provider_id} not found")

    def search_providers(self, **filters) -> List[HealthcareProvider]:
        query = HealthcareProviderProfile.objects.filter(is_verified=True)
        
        if 'specialization' in filters:
            query = query.filter(specializations__contains=[filters['specialization']])
        
        if 'facility_id' in filters:
            query = query.filter(facilities__id=filters['facility_id'])
        
        return [self._model_to_entity(p) for p in query]

    def _model_to_entity(self, model: HealthcareProviderProfile) -> HealthcareProvider:
        return HealthcareProvider(
            id=model.id,
            user_id=model.user_id,
            specializations=model.specializations,
            license_number=model.license_number,
            facilities=model.facilities.values_list('id', flat=True),
            available_hours=model.available_hours,
            languages=model.languages,
            is_verified=model.is_verified
        )