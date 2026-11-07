from django.contrib import admin
from .models import ConsultationRequest, QuoteRequest

class LeadAdminMixin:
    list_filter = ("status", "province", "created_at")
    search_fields = ("tracking_code", "full_name", "phone", "province", "city")
    readonly_fields = ("tracking_code", "created_at", "updated_at")
    date_hierarchy = "created_at"

@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(LeadAdminMixin, admin.ModelAdmin):
    list_display = ("tracking_code", "full_name", "phone", "province", "crop_type", "status", "created_at")

@admin.register(QuoteRequest)
class QuoteRequestAdmin(LeadAdminMixin, admin.ModelAdmin):
    list_display = ("tracking_code", "full_name", "phone", "product_name_snapshot", "quantity", "status", "created_at")
    readonly_fields = LeadAdminMixin.readonly_fields + ("product_name_snapshot", "unit_snapshot")
