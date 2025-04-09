# modules/community_hub/infrastructure/models/events.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel


class CommunityEventModel(BaseModel):
    """Модель мероприятия сообщества"""

    class Status(models.TextChoices):
        PLANNED = 'planned', _('Planned')
        ONGOING = 'ongoing', _('Ongoing')
        COMPLETED = 'completed', _('Completed')
        CANCELLED = 'cancelled', _('Cancelled')

    community = models.ForeignKey(
        'communities.CommunityModel',
        on_delete=models.CASCADE,
        related_name='events'
    )
    title = models.CharField(
        _('Title'),
        max_length=200
    )
    description = models.TextField(
        _('Description'),
        max_length=10000
    )
    organizer = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='organized_events'
    )
    start_time = models.DateTimeField(
        _('Start time'),
        db_index=True
    )
    end_time = models.DateTimeField(
        _('End time')
    )
    location = models.CharField(
        _('Location'),
        max_length=200
    )
    status = models.CharField(
        _('Status'),
        max_length=10,
        choices=Status.choices,
        default=Status.PLANNED
    )
    max_participants = models.PositiveIntegerField(
        _('Max participants'),
        null=True,
        blank=True
    )
    is_online = models.BooleanField(
        _('Is online'),
        default=False
    )
    cover_image_url = models.URLField(
        _('Cover image URL'),
        max_length=512,
        null=True,
        blank=True
    )
    tags = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True
    )
    participants = models.ManyToManyField(
        'users.User',
        through='EventParticipation',
        related_name='events_participated'
    )

    class Meta:
        verbose_name = _('Community Event')
        verbose_name_plural = _('Community Events')
        indexes = [
            models.Index(fields=['community']),
            models.Index(fields=['start_time']),
            models.Index(fields=['status']),
            models.Index(fields=['is_online']),
        ]
        ordering = ['start_time']

    def __str__(self):
        return f"{self.title} at {self.community} ({self.get_status_display()})"


class EventParticipation(models.Model):
    """Модель участия в мероприятии"""
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        CommunityEventModel,
        on_delete=models.CASCADE
    )
    registered_at = models.DateTimeField(
        auto_now_add=True
    )
    attended = models.BooleanField(
        default=False
    )
    feedback = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ('user', 'event')


class CommunityPostModel(BaseModel):
    """Модель публикации в сообществе"""

    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PUBLISHED = 'published', _('Published')
        ARCHIVED = 'archived', _('Archived')
        REMOVED = 'removed', _('Removed')

    community = models.ForeignKey(
        'communities.CommunityModel',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='community_posts'
    )
    title = models.CharField(
        _('Title'),
        max_length=200
    )
    content = models.TextField(
        _('Content'),
        max_length=20000
    )
    status = models.CharField(
        _('Status'),
        max_length=10,
        choices=Status.choices,
        default=Status.PUBLISHED
    )
    like_count = models.PositiveIntegerField(
        _('Like count'),
        default=0
    )
    comment_count = models.PositiveIntegerField(
        _('Comment count'),
        default=0
    )
    is_pinned = models.BooleanField(
        _('Is pinned'),
        default=False
    )
    moderator = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='moderated_posts'
    )
    moderation_reason = models.CharField(
        _('Moderation reason'),
        max_length=500,
        null=True,
        blank=True
    )
    tags = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True
    )
    attachments = ArrayField(
        models.URLField(max_length=512),
        default=list,
        blank=True
    )

    class Meta:
        verbose_name = _('Community Post')
        verbose_name_plural = _('Community Posts')
        indexes = [
            models.Index(fields=['community']),
            models.Index(fields=['author']),
            models.Index(fields=['status']),
            models.Index(fields=['is_pinned']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author} in {self.community}"