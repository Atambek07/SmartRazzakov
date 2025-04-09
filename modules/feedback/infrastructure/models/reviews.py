# modules/feedback/infrastructure/models/reviews.py
from django.db import models
from core.models.base import BaseModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Review(BaseModel):
    class ReviewStatus(models.TextChoices):
        PENDING = 'pending', 'На модерации'
        APPROVED = 'approved', 'Одобрено'
        REJECTED = 'rejected', 'Отклонено'
        ARCHIVED = 'archived', 'Архивировано'

    author = models.ForeignKey(
        'core.User', 
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        verbose_name='Тип контента'
    )
    object_id = models.PositiveIntegerField(
        verbose_name='ID объекта'
    )
    content_object = GenericForeignKey(
        'content_type', 
        'object_id'
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name='Оценка'
    )
    text = models.TextField(
        null=True, 
        blank=True,
        verbose_name='Текст отзыва'
    )
    audio = models.FileField(
        upload_to='reviews/audio/%Y/%m/%d/',
        null=True,
        blank=True
    )
    video = models.FileField(
        upload_to='reviews/video/%Y/%m/%d/',
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=ReviewStatus.choices,
        default=ReviewStatus.PENDING,
        verbose_name='Статус'
    )
    source_module = models.CharField(
        max_length=50,
        verbose_name='Источник'
    )
    helpful_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Полезные голоса'
    )
    reply_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Ответы'
    )

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['author', 'status']),
            models.Index(fields=['rating', 'created_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'content_type', 'object_id'],
                name='unique_user_review_per_object'
            )
        ]

    def __str__(self):
        return f"Отзыв #{self.id} от {self.author}"

class ReviewImage(BaseModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='reviews/images/%Y/%m/%d/',
        verbose_name='Изображение'
    )
    caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Подпись'
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name='Проверено'
    )

    class Meta:
        verbose_name = 'Изображение отзыва'
        verbose_name_plural = 'Изображения отзывов'

class ReviewTag(BaseModel):
    name = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name='Название тега'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    reviews = models.ManyToManyField(
        Review,
        related_name='tags',
        blank=True
    )
    usage_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Частота использования'
    )
                            
    class Meta:
        verbose_name = 'Тег отзыва'
        verbose_name_plural = 'Теги отзывов'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name                                                                                                        