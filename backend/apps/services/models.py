from django.db import models
from apps.core.models import PublishableModel

class Service(PublishableModel):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(max_length=220, unique=True, allow_unicode=True, verbose_name="نامک")
    summary = models.CharField(max_length=300, blank=True, verbose_name="خلاصه")
    description = models.TextField(verbose_name="توضیحات")
    is_featured = models.BooleanField(default=False, db_index=True, verbose_name="ویژه")
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="ترتیب")

    class Meta:
        ordering = ["sort_order", "title"]
        verbose_name = "خدمت"
        verbose_name_plural = "خدمات"

    def __str__(self):
        return self.title
