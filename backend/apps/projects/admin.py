from django.contrib import admin
from .models import Project, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "completed_on", "publication_status", "is_featured", "is_demo")
    list_filter = ("publication_status", "is_featured", "is_demo")
    search_fields = ("title", "location", "challenge", "actions", "results")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (ProjectImageInline,)
