from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from uuid import uuid4

class UserRole(models.TextChoices):
    STUDENT = 'student', 'Ученик'
    TEACHER = 'teacher', 'Учитель'
    TUTOR = 'tutor', 'Репетитор'
    PARENT = 'parent', 'Родитель'
    ADMIN = 'admin', 'Администратор'

class UserProfileModel(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
        verbose_name='Роль'
    )
    grade_level = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Класс обучения'
    )
    subjects = ArrayField(
        models.CharField(max_length=50),
        default=list,
        verbose_name='Предметы'
    )
    achievements = ArrayField(
        models.CharField(max_length=100),
        default=list,
        verbose_name='Достижения'
    )
    metadata = models.JSONField(
        default=dict,
        verbose_name='Дополнительные данные'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        indexes = [
            models.Index(fields=['role', 'grade_level']),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()