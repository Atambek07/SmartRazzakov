from django.db import models
from django.contrib.postgres.fields import JSONField
from uuid import uuid4

class ContentType(models.TextChoices):
    LESSON = 'lesson', 'Урок'
    TEST = 'test', 'Тест'
    VIDEO = 'video', 'Видео'
    EBOOK = 'ebook', 'Электронная книга'
    GAME = 'game', 'Игра'

class CourseLevel(models.TextChoices):
    BEGINNER = 'beginner', 'Начальный'
    INTERMEDIATE = 'intermediate', 'Средний'
    ADVANCED = 'advanced', 'Продвинутый'

class EducationalContentModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=200, verbose_name='Название')
    content_type = models.CharField(
        max_length=20,
        choices=ContentType.choices,
        verbose_name='Тип контента'
    )
    subject = models.CharField(max_length=100, verbose_name='Предмет')
    grade_level = models.IntegerField(verbose_name='Уровень класса')
    author = models.ForeignKey(
        'UserProfileModel',
        on_delete=models.CASCADE,
        related_name='authored_content',
        verbose_name='Автор'
    )
    file_url = models.URLField(max_length=500, verbose_name='Ссылка на файл')
    metadata = JSONField(default=dict, verbose_name='Метаданные')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Образовательный контент'
        verbose_name_plural = 'Образовательный контент'
        indexes = [
            models.Index(fields=['subject', 'grade_level']),
            models.Index(fields=['is_published']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_content_type_display()})"

class CourseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=200, verbose_name='Название курса')
    tutor = models.ForeignKey(
        'UserProfileModel',
        on_delete=models.CASCADE,
        related_name='tutored_courses',
        verbose_name='Преподаватель'
    )
    schedule = JSONField(verbose_name='Расписание')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоимость'
    )
    currency = models.CharField(
        max_length=3,
        default='KGZ',
        verbose_name='Валюта'
    )
    level = models.CharField(
        max_length=20,
        choices=CourseLevel.choices,
        verbose_name='Уровень сложности'
    )
    capacity = models.PositiveIntegerField(default=30, verbose_name='Вместимость')
    enrolled_students = models.ManyToManyField(
        'UserProfileModel',
        related_name='enrolled_courses',
        blank=True
    )
    rating = models.FloatField(default=0.0, verbose_name='Рейтинг')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        indexes = [
            models.Index(fields=['tutor', 'level']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_level_display()})"

class SchoolModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name='Название школы')
    address = models.TextField(verbose_name='Адрес')
    rating = models.FloatField(default=0.0, verbose_name='Рейтинг')
    available_seats = JSONField(
        default=dict,
        verbose_name='Доступные места по классам'
    )
    programs = models.JSONField(
        default=list,
        verbose_name='Образовательные программы'
    )
    photos = models.JSONField(
        default=list,
        verbose_name='Фотографии школы'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Школа'
        verbose_name_plural = 'Школы'

    def __str__(self):
        return self.name

class TestResultModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        'UserProfileModel',
        on_delete=models.CASCADE,
        related_name='test_results'
    )
    content = models.ForeignKey(
        EducationalContentModel,
        on_delete=models.CASCADE,
        related_name='results'
    )
    score = models.FloatField(verbose_name='Результат')
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = JSONField(default=dict, verbose_name='Дополнительные данные')

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'
        unique_together = ('user', 'content')

    def __str__(self):
        return f"{self.user} - {self.content}: {self.score}"