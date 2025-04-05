from django.db import models
from django.contrib.auth import get_user_model
from core.models import TimeStampedModel

User = get_user_model()

class Course(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.CharField(max_length=100)
    difficulty = models.CharField(
        max_length=20,
        choices=[(tag.value, tag.name) for tag in DifficultyLevel]
    )
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

class Lesson(TimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in ContentType])
    content_url = models.URLField()
    duration_minutes = models.IntegerField()
    order = models.PositiveIntegerField()

class ClassRoom(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    zoom_link = models.URLField(null=True)
    is_active = models.BooleanField(default=True)