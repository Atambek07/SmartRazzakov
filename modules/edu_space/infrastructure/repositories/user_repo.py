from uuid import UUID
from django.core.exceptions import ObjectDoesNotExist
from typing import List, Optional
from ...models import UserProfileModel, UserRole
from ....domain.entities import UserProfile
from ....domain.exceptions import UserNotFoundError

class DjangoUserRepository:
    """Реализация репозитория пользователей на Django ORM"""

    def _to_entity(self, model: UserProfileModel) -> UserProfile:
        """Преобразует Django модель в доменную сущность"""
        return UserProfile(
            id=model.id,
            role=UserRole(model.role),
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            grade_level=model.grade_level,
            subjects=model.subjects,
            achievements=model.achievements,
            metadata=model.metadata
        )

    def _to_model(self, entity: UserProfile) -> UserProfileModel:
        """Преобразует доменную сущность в Django модель"""
        return UserProfileModel(
            id=entity.id,
            role=entity.role.value,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            grade_level=entity.grade_level,
            subjects=entity.subjects,
            achievements=entity.achievements,
            metadata=entity.metadata
        )

    def get_by_id(self, user_id: UUID) -> UserProfile:
        try:
            model = UserProfileModel.objects.get(pk=user_id)
            return self._to_entity(model)
        except ObjectDoesNotExist:
            raise UserNotFoundError(f"User with id {user_id} not found")

    def search_users(
        self,
        role: Optional[UserRole] = None,
        subjects: Optional[List[str]] = None,
        grade_level: Optional[int] = None
    ) -> List[UserProfile]:
        queryset = UserProfileModel.objects.all()

        if role:
            queryset = queryset.filter(role=role.value)
        if subjects:
            queryset = queryset.filter(subjects__contains=subjects)
        if grade_level:
            queryset = queryset.filter(grade_level=grade_level)

        return [self._to_entity(user) for user in queryset]

    def update_profile(self, user: UserProfile) -> None:
        UserProfileModel.objects.filter(pk=user.id).update(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            grade_level=user.grade_level,
            subjects=user.subjects,
            achievements=user.achievements,
            metadata=user.metadata
        )

    def get_tutors_by_subject(self, subject: str) -> List[UserProfile]:
        queryset = UserProfileModel.objects.filter(
            role=UserRole.TUTOR.value,
            subjects__contains=[subject]
        )
        return [self._to_entity(tutor) for tutor in queryset]