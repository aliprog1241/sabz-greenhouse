from django.contrib import admin
from apps.core.admin_mixins import PublishableAdminMixin
from .models import Service

@admin.register(Service)
class ServiceAdmin(PublishableAdminMixin, admin.ModelAdmin):
    list_display = ("title", "publication_status", "is_featured", "sort_order", "updated_at")
    list_filter = ("publication_status", "is_featured")
    search_fields = ("title", "summary", "description")
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 50
