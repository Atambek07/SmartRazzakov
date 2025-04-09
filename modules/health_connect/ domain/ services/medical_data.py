# modules/health_connect/domain/services/medical_data.py
from typing import List, Optional
from ...entities import MedicalRecord
from ....core.utils.security import DataEncryptor
from ..exceptions import PermissionDenied, InvalidMedicalData
from ....core.integrations.storage import CloudStorageClient

class MedicalDataService:
    def __init__(self,
                 repository: 'MedicalRecordRepository',
                 storage: CloudStorageClient,
                 encryptor: DataEncryptor):
        self.repo = repository
        self.storage = storage
        self.encryptor = encryptor

    def get_records(self, patient_id: str, 
                  requester_id: str) -> List[MedicalRecord]:
        """Получение записей с проверкой прав доступа"""
        if patient_id != requester_id:
            raise PermissionDenied("Access to medical records denied")
        
        records = self.repo.get_by_patient(patient_id)
        return [self._decrypt_record(r) for r in records]

    def add_record(self, record: MedicalRecord) -> MedicalRecord:
        """Добавление новой медицинской записи"""
        self._validate_record(record)
        encrypted = self._encrypt_record(record)
        return self.repo.save(encrypted)

    def share_record(self, record_id: str, provider_id: str) -> None:
        """Предоставление доступа к записи врачу"""
        record = self.repo.get_by_id(record_id)
        if provider_id not in record.authorized_providers:
            updated = record.copy(update={
                'authorized_providers': [*record.authorized_providers, provider_id]
            })
            self.repo.save(updated)

    def _validate_record(self, record: MedicalRecord) -> None:
        """Проверка валидности медицинских данных"""
        if record.record_type == 'allergy' and not record.description:
            raise InvalidMedicalData("Allergy description required")
        
        if record.date > datetime.now():
            raise InvalidMedicalData("Future dates not allowed")

    def _encrypt_record(self, record: MedicalRecord) -> MedicalRecord:
        """Шифрование конфиденциальных данных"""
        if record.is_confidential:
            return record.copy(update={
                'description': self.encryptor.encrypt(record.description),
                'attachments': [self.storage.upload(a) for a in record.attachments]
            })
        return record

    def _decrypt_record(self, record: MedicalRecord) -> MedicalRecord:
        """Дешифровка данных для авторизованного доступа"""
        if record.is_confidential:
            return record.copy(update={
                'description': self.encryptor.decrypt(record.description),
                'attachments': [self.storage.get_url(a) for a in record.attachments]
            })
        return record