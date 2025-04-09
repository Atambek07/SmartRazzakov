from uuid import UUID
from django.core.exceptions import ObjectDoesNotExist
from ...models import EducationalContentModel, ContentType
from ....domain.entities import EducationalContent
from ....domain.exceptions import ContentNotFoundError

class DjangoContentRepository:
    """Реализация репозитория контента на Django ORM"""

    def _to_entity(self, model: EducationalContentModel) -> EducationalContent:
        """Преобразует Django модель в доменную сущность"""
        return EducationalContent(
            id=model.id,
            title=model.title,
            content_type=ContentType(model.content_type),
            subject=model.subject,
            grade_level=model.grade_level,
            author_id=model.author_id,
            file_url=model.file_url,
            metadata=model.metadata,
            is_published=model.is_published,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: EducationalContent) -> EducationalContentModel:
        """Преобразует доменную сущность в Django модель"""
        return EducationalContentModel(
            id=entity.id,
            title=entity.title,
            content_type=entity.content_type.value,
            subject=entity.subject,
            grade_level=entity.grade_level,
            author_id=entity.author_id,
            file_url=entity.file_url,
            metadata=entity.metadata,
            is_published=entity.is_published
        )

    def add(self, content: EducationalContent) -> EducationalContent:
        model = self._to_model(content)
        model.save()
        return self._to_entity(model)

    def get_by_id(self, content_id: UUID) -> EducationalContent:
        try:
            model = EducationalContentModel.objects.get(pk=content_id)
            return self._to_entity(model)
        except ObjectDoesNotExist:
            raise ContentNotFoundError(f"Content with id {content_id} not found")

    def update(self, content: EducationalContent) -> None:
        EducationalContentModel.objects.filter(pk=content.id).update(
            title=content.title,
            content_type=content.content_type.value,
            subject=content.subject,
            grade_level=content.grade_level,
            file_url=content.file_url,
            metadata=content.metadata,
            is_published=content.is_published
        )

    def list_by_subject(self, subject: str, grade_level: int) -> list[EducationalContent]:
        queryset = EducationalContentModel.objects.filter(
            subject=subject,
            grade_level=grade_level,
            is_published=True
        ).order_by('-created_at')
        
        return [self._to_entity(model) for model in queryset]