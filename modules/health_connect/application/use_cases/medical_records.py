# modules/health_connect/application/use_cases/medical_records.py
from typing import List, Optional
from ...domain.entities import MedicalRecord
from ...domain.services.medical_data import MedicalDataService
from ..dto.medical_dto import (
    MedicalRecordCreate, 
    MedicalRecordUpdate,
    MedicalRecordResponse,
    MedicalRecordSearch
)
from ..mappers import medical_mapper
from core.utils.logging import LoggingService
from core.utils.responses import ApplicationResponse

class MedicalRecordUseCases:
    def __init__(self, 
                 medical_data_service: MedicalDataService,
                 logger: LoggingService):
        self.medical_data = medical_data_service
        self.logger = logger

class CreateMedicalRecordUseCase(MedicalRecordUseCases):
    def execute(self, dto: MedicalRecordCreate) -> ApplicationResponse:
        try:
            record = medical_mapper.dto_to_entity(dto)
            created_record = self.medical_data.add_record(record)
            response_dto = medical_mapper.entity_to_dto(created_record)
            return ApplicationResponse.success(response_dto)
        
        except InvalidMedicalData as e:
            self.logger.error(f"Invalid medical data: {str(e)}")
            return ApplicationResponse.error("Invalid medical data", code=400)
        
        except Exception as e:
            self.logger.critical(f"Medical record creation failed: {str(e)}")
            return ApplicationResponse.error("Internal server error", code=500)

class UpdateMedicalRecordUseCase(MedicalRecordUseCases):
    def execute(self, record_id: str, dto: MedicalRecordUpdate) -> ApplicationResponse:
        try:
            existing = self.medical_data.get_record(record_id)
            updated_data = medical_mapper.update_entity(existing, dto)
            updated_record = self.medical_data.update_record(updated_data)
            return ApplicationResponse.success(
                medical_mapper.entity_to_dto(updated_record)
            )
        
        except MedicalRecordNotFound:
            return ApplicationResponse.error("Record not found", code=404)
        
        except PermissionDenied:
            return ApplicationResponse.error("Access denied", code=403)

class GetMedicalRecordsUseCase(MedicalRecordUseCases):
    def execute(self, search: MedicalRecordSearch) -> ApplicationResponse:
        try:
            records = self.medical_data.search_records(
                patient_id=search.patient_id,
                record_type=search.record_type,
                start_date=search.start_date,
                end_date=search.end_date,
                keywords=search.keywords
            )
            dtos = [medical_mapper.entity_to_dto(r) for r in records]
            return ApplicationResponse.success(dtos)
        
        except InvalidMedicalData as e:
            return ApplicationResponse.error(str(e), code=400)