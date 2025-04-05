from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    FEEDBACK_TYPES = [
        ('service', 'Сервис'),
        ('product', 'Продукт'),
        ('government', 'Госучреждение'),
        ('transport', 'Транспорт')
    ]

    STATUS_CHOICES = [
        ('pending', 'На модерации'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено')
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    target_id = models.CharField(max_length=100)  # ID бизнеса/сервиса
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()  # 1-5
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    photos = models.JSONField(default=list)  # Список URL фотографий

    class Meta:
        indexes = [
            models.Index(fields=['target_id']),
            models.Index(fields=['author']),
        ]


class Rating(models.Model):
    target_id = models.CharField(max_length=100, unique=True)
    average = models.FloatField()
    count = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)