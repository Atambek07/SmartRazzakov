# modules/made_in_leylek/made_in_leylek/admin.py
from django.contrib import admin
from .infrastructure.models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'seller_id')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('seller_id', 'name', 'description')}),
        ('Pricing', {'fields': ('category', 'price', 'quantity')}),
        ('Dates', {'fields': ('production_date', 'expiration_date')}),
        ('Metadata', {'fields': ('tags', 'rating', 'created_at', 'updated_at')}),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'total_amount', 'user_id', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user_id', 'tracking_number')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('user_id', 'status')}),
        ('Order Details', {'fields': ('items', 'total_amount')}),
        ('Delivery', {'fields': ('delivery_info', 'tracking_number')}),
        ('Comments', {'fields': ('buyer_comment',)}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )