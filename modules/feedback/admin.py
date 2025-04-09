# modules/feedback/admin.py
from django.contrib import admin
from .models import Review, ReviewImage, ReviewTag, RatingSnapshot, ReviewVote
from .application.dto import ReviewResponseDTO

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'truncated_text', 'author', 'rating', 'status', 'created_at')
    list_filter = ('status', 'source_module', 'content_type')
    search_fields = ('text', 'author__email')
    readonly_fields = ('content_object',)
    actions = ['approve_selected', 'reject_selected']

    def truncated_text(self, obj):
        return obj.text[:50] + '...' if obj.text else ''
    truncated_text.short_description = 'Текст'

    @admin.action(description="Одобрить выбранные отзывы")
    def approve_selected(self, request, queryset):
        queryset.update(status=Review.ReviewStatus.APPROVED)

    @admin.action(description="Отклонить выбранные отзывы")
    def reject_selected(self, request, queryset):
        queryset.update(status=Review.ReviewStatus.REJECTED)

@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'image_tag')
    readonly_fields = ('image_tag',)

@admin.register(ReviewTag)
class ReviewTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'usage_count')
    search_fields = ('name',)

@admin.register(RatingSnapshot)
class RatingSnapshotAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'average_rating', 'calculated_at')
    readonly_fields = ('content_object',)

@admin.register(ReviewVote)
class ReviewVoteAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'vote_type')
    list_filter = ('vote_type',)