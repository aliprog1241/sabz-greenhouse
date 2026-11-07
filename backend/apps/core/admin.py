from django.contrib import admin
from .models import Certificate, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "specialist_name", "phone", "updated_at")

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer", "issued_on", "publication_status", "is_demo")
    list_filter = ("publication_status", "is_demo")
    search_fields = ("title", "issuer", "description")
