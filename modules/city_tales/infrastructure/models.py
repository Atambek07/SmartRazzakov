from django.db import models
from django.contrib.auth import get_user_model
from core.models import TimeStampedModel

User = get_user_model()

class StoryModel(TimeStampedModel):
    title = models.CharField(max_length=200)
    content = models.JSONField()  # {text: str, audio: str}
    content_type = models.CharField(max_length=10, choices=[
        ('text', 'Text'),
        ('audio', 'Audio'),
        ('mixed', 'Mixed')
    ])
    location = models.CharField(max_length=100)  # "lat,lng"
    qr_code = models.ImageField(upload_to='qr_codes/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Story: {self.title}"