from rest_framework import serializers
from ..infrastructure.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content_type', 'content_url', 'duration_minutes', 'order']


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    difficulty = serializers.ChoiceField(choices=[(tag.value, tag.name) for tag in DifficultyLevel])

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'subject', 'difficulty', 'is_free', 'price', 'lessons']