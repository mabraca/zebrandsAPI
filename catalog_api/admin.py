from django.contrib import admin
from .models import Product, Log

"""
Class ProductAdmin and Class LogAdmin manage admin interface for Product model and Log model respectively.
"""


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'sku', 'name', 'price', 'brand', 'is_active')
    list_filter = ('name', 'brand', 'is_active')
    search_fields = ('sku', 'name', 'brand')

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # When the user wants to delete a product don't delete trace, just deactivate
        obj.is_active = False
        obj.modified_by = request.user
        obj.save()

    def delete_queryset(self, request, queryset):
        # When the user wants to delete a product don't delete trace, just deactivate
        for obj in queryset:
            obj.is_active = False
            obj.modified_by = request.user
            obj.save()


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'action', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('product__name', 'user__username')
