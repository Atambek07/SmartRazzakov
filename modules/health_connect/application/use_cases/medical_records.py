from ..domain.entities import MedicalRecord
from ..domain.services import MedicalDataService


class CreateMedicalRecordUseCase:
    def __init__(self, medical_repository, data_service: MedicalDataService):
        self.repo = medical_repository
        self.service = data_service

    def execute(self, dto: MedicalRecordDTO) -> MedicalRecord:
        """Создает новую медицинскую запись с проверкой данных"""
        if not self.service.validate_diagnosis(dto.diagnosis):
            raise InvalidMedicalDataError("Некорректный диагноз")

        record = MedicalRecord(
            id=None,
            patient_id=dto.patient_id,
            diagnosis=dto.diagnosis,
            treatment=dto.treatment,
            doctor_id=dto.doctor_id,
            date=datetime.now(),
            is_emergency=dto.is_emergency
        )

        return self.repo.save(record)