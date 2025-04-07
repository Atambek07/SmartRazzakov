from django.db import models
from django.contrib.postgres.fields import ArrayField
from enum import Enum

class ContentFormat(models.TextChoices):
    AUDIO = "audio", "Аудио"
    TEXT = "text", "Текст"
    VISUAL = "visual", "Визуал"

class TaleContentModel(models.Model):
    """Модель хранения контента достопримечательностей в PostgreSQL."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    location_id = models.CharField(max_length=36)  # Связь с достопримечательностью
    author_id = models.CharField(max_length=36)  # ID создателя контента
    audio_url = models.URLField(max_length=512, null=True, blank=True)
    text_content = models.TextField(null=True, blank=True)
    images = ArrayField(models.URLField(max_length=512), default=list)
    qr_code = models.CharField(max_length=64, unique=True)
    language = models.CharField(max_length=8, default="ru")
    duration_minutes = models.FloatField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tale_contents"
        indexes = [
            models.Index(fields=["qr_code"]),
            models.Index(fields=["location_id"]),
        ]

class UserPreferencesModel(models.Model):
    """Модель хранения предпочтений пользователей."""
    user_id = models.CharField(max_length=36, primary_key=True)
    preferred_format = models.CharField(
        max_length=16,
        choices=ContentFormat.choices,
        default=ContentFormat.TEXT
    )
    preferred_language = models.CharField(max_length=8, default="ru")
    last_used_qr = models.CharField(max_length=64, null=True, blank=True)
    font_size = models.IntegerField(default=16)
    high_contrast = models.BooleanField(default=False)

    class Meta:
        db_table = "user_preferences"