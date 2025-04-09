# modules/gov_connect/domain/services/document_service.py
from io import BytesIO
from typing import Union
from reportlab.pdfgen import canvas
from ...domain.entities import Document
from core.utils.file_processing import validate_file_type

class DocumentService:
    def __init__(self, storage_adapter):
        self.storage = storage_adapter

    def upload_document(
        self,
        file_data: bytes,
        filename: str,
        user_id: UUID,
        complaint_id: Optional[UUID] = None
    ) -> Document:
        """Загрузка документа с валидацией"""
        if not validate_file_type(file_data, filename):
            raise ValueError("Invalid file type")

        document = Document(
            user_id=user_id,
            complaint_id=complaint_id,
            filename=filename,
            size=len(file_data))
        
        storage_path = self.storage.upload(
            content=file_data,
            path=f"documents/{user_id}/{document.id}"
        )
        document.storage_path = storage_path
        return self.repo.save(document)

    def generate_complaint_report(self, complaint: Complaint) -> BytesIO:
        """Генерация PDF-отчета по жалобе"""
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        
        p.drawString(100, 800, f"Жалоба #{complaint.tracking_code}")
        p.drawString(100, 780, f"Статус: {complaint.status.value}")
        p.drawString(100, 760, f"Дата создания: {complaint.created_at}")
        
        if complaint.status == 'RESOLVED':
            p.drawString(100, 740, "Описание решения:")
            p.drawString(120, 720, complaint.resolution_comment)

        p.save()
        buffer.seek(0)
        return buffer