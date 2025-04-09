# modules/gov_connect/infrastructure/repositories/complaint_repo.py
from typing import List, Optional
from uuid import UUID
from django.db import transaction
from django.contrib.gis.geos import Point
from ...domain.entities import Complaint as DomainComplaint
from ...domain.exceptions import ComplaintNotFoundError
from ..models import Complaint, ComplaintPhoto
import logging

logger = logging.getLogger(__name__)

class DjangoComplaintRepository:
    def __init__(self, geo_service=None):
        self.geo_service = geo_service

    @transaction.atomic
    def create(self, complaint: DomainComplaint) -> DomainComplaint:
        try:
            # Конвертация доменной сущности в Django модель
            db_complaint = Complaint.objects.create(
                user_id=complaint.user_id,
                title=complaint.title,
                description=complaint.description,
                location=Point(complaint.location.x, complaint.location.y),
                category=complaint.category,
                status=complaint.status.value
            )

            # Сохранение фотографий
            for photo_url in complaint.photo_urls:
                ComplaintPhoto.objects.create(
                    complaint=db_complaint,
                    photo_url=photo_url
                )

            return self._to_domain(db_complaint)
        except Exception as e:
            logger.error(f"Error creating complaint: {str(e)}")
            raise

    def update(self, complaint: DomainComplaint) -> DomainComplaint:
        try:
            db_complaint = Complaint.objects.get(id=complaint.id)
            db_complaint.title = complaint.title
            db_complaint.description = complaint.description
            db_complaint.status = complaint.status.value
            db_complaint.save()
            return self._to_domain(db_complaint)
        except Complaint.DoesNotExist:
            raise ComplaintNotFoundError()
        except Exception as e:
            logger.error(f"Error updating complaint: {str(e)}")
            raise

    def find_by_id(self, complaint_id: UUID) -> DomainComplaint:
        try:
            db_complaint = Complaint.objects.prefetch_related('photos').get(id=complaint_id)
            return self._to_domain(db_complaint)
        except Complaint.DoesNotExist:
            raise ComplaintNotFoundError()

    def find_similar(self, domain_complaint: DomainComplaint, radius: int = 500) -> List[DomainComplaint]:
        point = Point(domain_complaint.location.x, domain_complaint.location.y)
        queryset = Complaint.objects.filter(
            location__distance_lte=(point, radius),
            category=domain_complaint.category
        ).exclude(id=domain_complaint.id)

        return [self._to_domain(c) for c in queryset]

    def _to_domain(self, db_complaint: Complaint) -> DomainComplaint:
        return DomainComplaint(
            id=db_complaint.id,
            user_id=db_complaint.user_id,
            title=db_complaint.title,
            description=db_complaint.description,
            location=(db_complaint.location.x, db_complaint.location.y),
            category=db_complaint.category,
            status=db_complaint.status,
            photo_urls=[p.photo_url for p in db_complaint.photos.all()],
            created_at=db_complaint.created_at,
            updated_at=db_complaint.updated_at
        )