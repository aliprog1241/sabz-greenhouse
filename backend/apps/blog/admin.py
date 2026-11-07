from django.contrib import admin
from apps.core.admin_mixins import PublishableAdminMixin
from .models import Article

@admin.register(Article)
class ArticleAdmin(PublishableAdminMixin, admin.ModelAdmin):
    list_display = ("title", "publication_status", "published_at", "is_demo", "updated_at")
    list_filter = ("publication_status", "is_demo")
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    list_per_page = 50
