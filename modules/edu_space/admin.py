from django.contrib import admin
from .infrastructure.models import (
    EducationalContentModel,
    CourseModel,
    SchoolModel,
    TestResultModel,
    UserProfileModel
)

class EducationalContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'subject', 'grade_level', 'author', 'is_published')
    list_filter = ('content_type', 'subject', 'grade_level', 'is_published')
    search_fields = ('title', 'subject')
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    actions = ['publish_selected']

    def publish_selected(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f"{updated} материалов опубликовано")
    publish_selected.short_description = "Опубликовать выбранные материалы"

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'tutor', 'level', 'price', 'currency', 'capacity', 'enrollment_count')
    list_select_related = ('tutor',)
    filter_horizontal = ('enrolled_students',)
    
    def enrollment_count(self, obj):
        return obj.enrolled_students.count()
    enrollment_count.short_description = 'Записанные студенты'

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'rating', 'programs_list')
    
    def programs_list(self, obj):
        return ", ".join(obj.programs[:3]) + ("..." if len(obj.programs) > 3 else "")
    programs_list.short_description = 'Программы'

class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'score', 'timestamp')
    list_filter = ('content__subject', 'timestamp')
    search_fields = ('user__username', 'content__title')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'grade_level', 'subjects_list')
    list_filter = ('role', 'grade_level')
    search_fields = ('username', 'first_name', 'last_name')
    filter_horizontal = ('groups', 'user_permissions')
    
    def subjects_list(self, obj):
        return ", ".join(obj.subjects[:3]) + ("..." if len(obj.subjects) > 3 else "")
    subjects_list.short_description = 'Предметы'

# Регистрация моделей
admin.site.register(EducationalContentModel, EducationalContentAdmin)
admin.site.register(CourseModel, CourseAdmin)
admin.site.register(SchoolModel, SchoolAdmin)
admin.site.register(TestResultModel, TestResultAdmin)
admin.site.register(UserProfileModel, UserProfileAdmin)