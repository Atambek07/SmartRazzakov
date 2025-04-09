# modules/gov_connect/infrastructure/models/services.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

class ServiceCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Название категории')
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=_('Идентификатор')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Описание')
    )

    class Meta:
        verbose_name = _('Категория услуг')
        verbose_name_plural = _('Категории услуг')

    def __str__(self):
        return self.name

class GovernmentService(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Название услуги')
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.PROTECT,
        related_name='services',
        verbose_name=_('Категория')
    )
    description = models.TextField(
        verbose_name=_('Описание услуги')
    )
    required_documents = models.JSONField(
        default=list,
        verbose_name=_('Необходимые документы')
    )
    online_available = models.BooleanField(
        default=False,
        verbose_name=_('Доступно онлайн')
    )
    offices = models.ManyToManyField(
        'municipal.GovernmentOffice',
        related_name='services',
        verbose_name=_('Офисы оказания')
    )
    average_rating = models.FloatField(
        default=0.0,
        verbose_name=_('Средний рейтинг')
    )
    status = models.BooleanField(
        default=True,
        verbose_name=_('Активна')
    )

    class Meta:
        verbose_name = _('Государственная услуга')
        verbose_name_plural = _('Государственные услуги')
        indexes = [
            models.Index(fields=['category', 'online_available']),
        ]

    def __str__(self):
        return f"{self.name} ({self.category})"