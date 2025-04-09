# modules/community_hub/infrastructure/models/communities.py
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel


class CommunityModel(BaseModel):
    """Модель сообщества в базе данных"""

    class Category(models.TextChoices):
        PROFESSIONAL = 'professional', _('Professional')
        HOBBY = 'hobby', _('Hobby')
        NEIGHBORHOOD = 'neighborhood', _('Neighborhood')
        CRISIS = 'crisis', _('Crisis Support')
        EDUCATION = 'education', _('Education')
        BUSINESS = 'business', _('Business')

    name = models.CharField(
        _('Name'),
        max_length=100,
        unique=True,
        db_index=True
    )
    description = models.TextField(
        _('Description'),
        max_length=2000
    )
    category = models.CharField(
        _('Category'),
        max_length=20,
        choices=Category.choices,
        default=Category.NEIGHBORHOOD
    )
    creator = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='created_communities'
    )
    members_count = models.PositiveIntegerField(
        _('Members count'),
        default=0
    )
    is_public = models.BooleanField(
        _('Is public'),
        default=True
    )
    rules = models.TextField(
        _('Rules'),
        max_length=5000,
        null=True,
        blank=True
    )
    avatar_url = models.URLField(
        _('Avatar URL'),
        max_length=512,
        null=True,
        blank=True
    )
    tags = ArrayField(
        models.CharField(max_length=50),
        size=15,
        default=list,
        blank=True
    )
    location = models.CharField(
        _('Location'),
        max_length=100,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        _('Is active'),
        default=True
    )
    metadata = JSONField(
        _('Metadata'),
        default=dict,
        blank=True
    )

    class Meta:
        verbose_name = _('Community')
        verbose_name_plural = _('Communities')
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['is_public']),
            models.Index(fields=['tags']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class CommunityMemberModel(BaseModel):
    """Модель участника сообщества"""

    class Role(models.TextChoices):
        MEMBER = 'member', _('Member')
        MODERATOR = 'moderator', _('Moderator')
        ADMIN = 'admin', _('Administrator')
        CREATOR = 'creator', _('Creator')

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='community_memberships'
    )
    community = models.ForeignKey(
        CommunityModel,
        on_delete=models.CASCADE,
        related_name='members'
    )
    role = models.CharField(
        _('Role'),
        max_length=10,
        choices=Role.choices,
        default=Role.MEMBER
    )
    contributions = models.PositiveIntegerField(
        _('Contributions'),
        default=0
    )
    last_active = models.DateTimeField(
        _('Last active'),
        null=True,
        blank=True
    )
    badges = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True
    )

    class Meta:
        verbose_name = _('Community Member')
        verbose_name_plural = _('Community Members')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'community'],
                name='unique_community_membership'
            )
        ]
        indexes = [
            models.Index(fields=['user', 'community']),
            models.Index(fields=['role']),
        ]

    def __str__(self):
        return f"{self.user} in {self.community} as {self.get_role_display()}"

class ChatMessageModel(BaseModel):
    """Модель сообщения в чате сообщества"""
    community = models.ForeignKey(
        CommunityModel,
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    text = models.TextField(
        _('Message text'),
        max_length=2000
    )
    is_read = models.BooleanField(
        _('Is read'),
        default=False
    )

    class Meta:
        verbose_name = _('Chat Message')
        verbose_name_plural = _('Chat Messages')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['community', 'created_at']),
        ]

    def __str__(self):
        return f"Message from {self.user} in {self.community}"