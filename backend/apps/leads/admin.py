from django.contrib import admin
from django.contrib import messages
from .models import ConsultationRequest, QuoteRequest

class LeadAdminMixin:
    list_filter = ("status", "province", "created_at")
    search_fields = ("tracking_code", "full_name", "phone", "province", "city")
    readonly_fields = ("tracking_code", "created_at", "updated_at")
    date_hierarchy = "created_at"
    list_per_page = 50
    ordering = ("-created_at",)
    actions = ("mark_as_contacted", "mark_as_in_progress", "mark_as_closed")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return self.readonly_fields
        editable_fields = {"status", "admin_notes"}
        return tuple(
            field.name
            for field in obj._meta.fields
            if field.name not in editable_fields
        )

    def _set_status(self, request, queryset, status, label):
        updated = queryset.update(status=status)
        self.message_user(
            request,
            f"وضعیت {updated} درخواست به «{label}» تغییر کرد.",
            messages.SUCCESS,
        )

    @admin.action(description="علامت‌گذاری به‌عنوان تماس گرفته‌شده")
    def mark_as_contacted(self, request, queryset):
        self._set_status(request, queryset, "CONTACTED", "تماس گرفته‌شده")

    @admin.action(description="علامت‌گذاری به‌عنوان در حال پیگیری")
    def mark_as_in_progress(self, request, queryset):
        self._set_status(request, queryset, "IN_PROGRESS", "در حال پیگیری")

    @admin.action(description="بستن درخواست‌های انتخاب‌شده")
    def mark_as_closed(self, request, queryset):
        self._set_status(request, queryset, "CLOSED", "بسته‌شده")

@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(LeadAdminMixin, admin.ModelAdmin):
    list_display = ("tracking_code", "full_name", "phone", "province", "crop_type", "status", "created_at")
    list_select_related = ("service",)

@admin.register(QuoteRequest)
class QuoteRequestAdmin(LeadAdminMixin, admin.ModelAdmin):
    list_display = ("tracking_code", "full_name", "phone", "product_name_snapshot", "quantity", "status", "created_at")
    readonly_fields = LeadAdminMixin.readonly_fields + ("product_name_snapshot", "unit_snapshot")
    list_select_related = ("product",)
