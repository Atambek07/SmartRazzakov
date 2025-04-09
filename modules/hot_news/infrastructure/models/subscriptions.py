from django.db import models
from django.contrib.postgres.fields import JSONField
from core.models import BaseModel
import uuid

class NewsSubscriptionModel(BaseModel):
    class LanguageChoices(models.TextChoices):
        RUSSIAN = 'ru', 'Русский'
        KYRGYZ = 'ky', 'Кыргызча'
        ENGLISH = 'en', 'English'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        'user_management.User',
        on_delete=models.CASCADE,
        related_name='news_subscriptions'
    )
    categories = JSONField(
        default=list,
        validators=[validate_categories]
    )
    notification_channels = JSONField(
        default=dict,
        validators=[validate_channels]
    )
    preferred_language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
        default=LanguageChoices.RUSSIAN
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='unique_user_subscription'
            )
        ]
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['categories']),
        ]
        verbose_name = 'News Subscription'
        verbose_name_plural = 'News Subscriptions'

    def __str__(self):
        return f"{self.user.email} subscriptions"

    def clean(self):
        super().clean()
        if not self.categories:
            raise ValidationError("At least one category required")

def validate_categories(value):
    valid_categories = dict(NewsArticleModel.CategoryChoices.choices)
    for category in value:
        if category not in valid_categories:
            raise ValidationError(f"Invalid category: {category}")

def validate_channels(value):
    required_keys = {'email', 'push', 'sms'}
    if not all(key in value for key in required_keys):
        raise ValidationError("Missing required notification channels")
    if not any(value.values()):
        raise ValidationError("At least one channel must be enabled")