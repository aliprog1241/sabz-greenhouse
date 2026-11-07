from django.contrib import admin
from .admin_mixins import PublishableAdminMixin
from .models import Certificate, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "specialist_name", "phone", "updated_at")
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Certificate)
class CertificateAdmin(PublishableAdminMixin, admin.ModelAdmin):
    list_display = ("title", "issuer", "issued_on", "publication_status", "is_demo")
    list_filter = ("publication_status", "is_demo")
    search_fields = ("title", "issuer", "description")
    date_hierarchy = "issued_on"
    list_per_page = 50
