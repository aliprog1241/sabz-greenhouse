from django.contrib import admin
from apps.core.admin_mixins import PublishableAdminMixin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(PublishableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "category", "brand", "unit", "is_active", "is_featured", "publication_status")
    list_filter = ("category", "is_active", "is_featured", "publication_status")
    search_fields = ("name", "sku", "brand", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = (ProductImageInline,)
    list_select_related = ("category",)
    list_per_page = 50
