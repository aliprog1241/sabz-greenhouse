from django.contrib import admin, messages

from .models import PublishableModel


class PublishableAdminMixin:
    """Shared, explicit publication actions for public-facing content."""

    actions = ("publish_selected", "move_selected_to_draft")

    @admin.action(description="انتشار موارد انتخاب‌شده")
    def publish_selected(self, request, queryset):
        updated = queryset.update(
            publication_status=PublishableModel.PublicationStatus.PUBLISHED
        )
        self.message_user(request, f"{updated} مورد منتشر شد.", messages.SUCCESS)

    @admin.action(description="بازگردانی موارد انتخاب‌شده به پیش‌نویس")
    def move_selected_to_draft(self, request, queryset):
        updated = queryset.update(
            publication_status=PublishableModel.PublicationStatus.DRAFT
        )
        self.message_user(
            request, f"{updated} مورد به پیش‌نویس بازگردانده شد.", messages.SUCCESS
        )
