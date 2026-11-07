from django.db import models
from apps.core.models import PublishableModel, TimeStampedModel

class Project(PublishableModel):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(max_length=220, unique=True, allow_unicode=True, verbose_name="نامک")
    location = models.CharField(max_length=200, blank=True, verbose_name="موقعیت")
    completed_on = models.DateField(null=True, blank=True, verbose_name="تاریخ تکمیل")
    challenge = models.TextField(blank=True, verbose_name="مسئله")
    actions = models.TextField(blank=True, verbose_name="اقدامات")
    results = models.TextField(blank=True, verbose_name="نتایج")
    is_featured = models.BooleanField(default=False, db_index=True, verbose_name="ویژه")
    is_demo = models.BooleanField(default=False, db_index=True, verbose_name="داده آزمایشی")

    class Meta:
        ordering = ["-completed_on", "title"]
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه‌ها"

    def __str__(self):
        return self.title

class ProjectImage(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images", verbose_name="پروژه")
    image = models.ImageField(upload_to="projects/", verbose_name="تصویر")
    alt_text = models.CharField(max_length=250, verbose_name="متن جایگزین")
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="ترتیب")

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "تصویر پروژه"
        verbose_name_plural = "تصاویر پروژه"
