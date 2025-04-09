# modules/gov_connect/infrastructure/models/complaints.py
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

User = get_user_model()

class ComplaintStatus(models.TextChoices):
    NEW = 'new', _('Новая')
    IN_PROGRESS = 'in_progress', _('В работе')
    RESOLVED = 'resolved', _('Решена')
    REJECTED = 'rejected', _('Отклонена')

class Complaint(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='complaints',
        verbose_name=_('Пользователь')
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_('Заголовок')
    )
    description = models.TextField(
        verbose_name=_('Подробное описание')
    )
    location = models.PointField(
        geography=True,
        srid=4326,
        verbose_name=_('Местоположение')
    )
    address = models.CharField(
        max_length=511,
        verbose_name=_('Адрес')
    )
    category = models.CharField(
        max_length=50,
        verbose_name=_('Категория')
    )
    status = models.CharField(
        max_length=20,
        choices=ComplaintStatus.choices,
        default=ComplaintStatus.NEW,
        verbose_name=_('Статус')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )
    related_complaints = models.ManyToManyField(
        'self',
        blank=True,
        verbose_name=_('Связанные жалобы')
    )
    votes = models.JSONField(
        default=dict,
        verbose_name=_('Реакции пользователей'),
        help_text=_('Счетчики лайков/дизлайков')
    )

    class Meta:
        verbose_name = _('Жалоба')
        verbose_name_plural = _('Жалобы')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.GIndex(fields=['location']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

class ComplaintPhoto(models.Model):
    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    photo_url = models.URLField(
        max_length=2048,
        verbose_name=_('Ссылка на фото')
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата загрузки')
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name=_('Проверено модератором')
    )

    class Meta:
        verbose_name = _('Фотография жалобы')
        verbose_name_plural = _('Фотографии жалоб')