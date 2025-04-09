# modules/feedback/infrastructure/models/ratings.py
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core.models.base import BaseModel

class RatingSnapshot(BaseModel):
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        'content_type', 
        'object_id'
    )
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name='Средний рейтинг'
    )
    total_reviews = models.PositiveIntegerField(
        verbose_name='Всего отзывов'
    )
    rating_distribution = models.JSONField(
        default=dict,
        verbose_name='Распределение оценок'
    )
    calculated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Рассчитано'
    )
    source_module = models.CharField(
        max_length=50,
        verbose_name='Модуль'
    )

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['calculated_at']),
        ]
        unique_together = ('content_type', 'object_id', 'calculated_at')

    def __str__(self):
        return f"Рейтинг {self.content_object} ({self.calculated_at})"

class ReviewVote(BaseModel):
    class VoteType(models.TextChoices):
        HELPFUL = 'helpful', 'Полезный'
        REPORT = 'report', 'Жалоба'

    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='votes'
    )
    user = models.ForeignKey(
        'core.User',
        on_delete=models.CASCADE,
        related_name='review_votes'
    )
    vote_type = models.CharField(
        max_length=10,
        choices=VoteType.choices,
        verbose_name='Тип голоса'
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'review'],
                name='unique_vote_per_user_review'
            )
        ]
        verbose_name = 'Голос за отзыв'
        verbose_name_plural = 'Голоса за отзывы'

    def __str__(self):
        return f"{self.vote_type} голос от {self.user}"