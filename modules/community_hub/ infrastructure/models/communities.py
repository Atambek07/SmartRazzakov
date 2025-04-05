from django.db import models
from django.contrib.auth import get_user_model
from core.models import TimeStampedModel

User = get_user_model()


class Community(TimeStampedModel):
    COMMUNITY_TYPES = [
        ('professional', 'Профессиональное'),
        ('hobby', 'Хобби'),
        ('neighborhood', 'Соседское'),
        ('crisis', 'Кризисное')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    community_type = models.CharField(max_length=20, choices=COMMUNITY_TYPES)
    is_public = models.BooleanField(default=True)
    rules = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='community_avatars/', null=True)

    def __str__(self):
        return f"{self.name} ({self.get_community_type_display()})"


class CommunityMember(models.Model):
    ROLES = [
        ('owner', 'Владелец'),
        ('moderator', 'Модератор'),
        ('member', 'Участник')
    ]

    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    reputation = models.IntegerField(default=0)

    class Meta:
        unique_together = ('community', 'user')