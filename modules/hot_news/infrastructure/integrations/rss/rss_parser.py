from django.db import models
from django.contrib.postgres.fields import ArrayField


class NewsArticle(models.Model):
    CATEGORY_CHOICES = [
        ('politics', 'Политика'),
        ('economy', 'Экономика'),
        ('culture', 'Культура'),
        ('emergency', 'Чрезвычайные ситуации'),
        ('transport', 'Транспорт')
    ]

    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
        ('critical', 'Критический')
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    publish_date = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    location = models.CharField(max_length=50, null=True, blank=True)
    related_links = ArrayField(models.URLField(), default=list)
    image_url = models.URLField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['priority']),
            models.Index(fields=['publish_date']),
        ]
        ordering = ['-publish_date']