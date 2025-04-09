# modules/gov_connect/admin.py
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .infrastructure.models import (
    Complaint,
    ComplaintPhoto,
    GovernmentService,
    ServiceCategory
)

@admin.register(Complaint)
class ComplaintAdmin(OSMGeoAdmin):
    list_display = ('truncated_title', 'status', 'category', 'user', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'user__email')
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def truncated_title(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    truncated_title.short_description = 'Заголовок'

@admin.register(ComplaintPhoto)
class ComplaintPhotoAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'uploaded_at', 'is_approved')
    list_editable = ('is_approved',)
    list_filter = ('is_approved', 'uploaded_at')
    raw_id_fields = ('complaint',)

class ServiceInline(admin.TabularInline):
    model = GovernmentService
    extra = 0
    fields = ('name', 'online_available', 'average_rating')
    readonly_fields = ('average_rating',)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'service_count')
    prepopulated_fields = {'slug': ('name',)}
    inlines = (ServiceInline,)
    
    def service_count(self, obj):
        return obj.services.count()
    service_count.short_description = 'Количество услуг'

@admin.register(GovernmentService)
class GovernmentServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'online_available', 'average_rating')
    list_filter = ('category', 'online_available')
    search_fields = ('name', 'description')
    filter_horizontal = ('offices',)
    readonly_fields = ('average_rating',)
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'description')
        }),
        ('Настройки', {
            'fields': ('online_available', 'required_documents', 'offices')
        }),
        ('Статистика', {
            'fields': ('average_rating', 'status')
        }),
    )