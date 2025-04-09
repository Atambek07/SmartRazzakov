from django.db import models
from django.contrib.postgres.fields import JSONField
from core.models import BaseModel
import uuid

class NewsArticleModel(BaseModel):
    class CategoryChoices(models.TextChoices):
        TRANSPORT = 'transport', 'Transport'
        EDUCATION = 'education', 'Education'
        CULTURE = 'culture', 'Culture'
        EMERGENCY = 'emergency', 'Emergency'
        GOVERNMENT = 'government', 'Government'
        COMMUNITY = 'community', 'Community'
        ECONOMY = 'economy', 'Economy'
        HEALTH = 'health', 'Health'
        OTHER = 'other', 'Other'

    class PriorityChoices(models.IntegerChoices):
        LOW = 1, 'Low'
        NORMAL = 2, 'Normal'
        HIGH = 3, 'High'
        CRITICAL = 4, 'Critical'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(5)]
    )
    content = models.TextField(
        validators=[MinLengthValidator(50)]
    )
    category = models.CharField(
        max_length=20,
        choices=CategoryChoices.choices,
        default=CategoryChoices.OTHER
    )
    priority = models.IntegerField(
        choices=PriorityChoices.choices,
        default=PriorityChoices.NORMAL
    )
    geo_location = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    sources = JSONField(
        default=list,
        validators=[validate_sources]
    )
    media_attachments = JSONField(
        default=list
    )
    sentiment_score = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(-1.0),
            MaxValueValidator(1.0)
        ]
    )
    views_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey(
        'user_management.User',
        on_delete=models.PROTECT,
        related_name='news_articles'
    )
    publish_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['category', 'priority']),
            models.Index(fields=['created_at']),
            models.Index(fields=['geo_location']),
        ]
        ordering = ['-publish_at']
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    def clean(self):
        super().clean()
        if self.priority == self.PriorityChoices.CRITICAL:
            if self.category != self.CategoryChoices.EMERGENCY:
                raise ValidationError(
                    "Critical priority allowed only for emergency category"
                )

def validate_sources(value):
    for source in value:
        if not source.startswith(('http://', 'https://', '/')):
            raise ValidationError('Invalid source format')