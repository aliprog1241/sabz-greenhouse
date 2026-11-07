from django.db import models
from apps.core.models import PublishableModel

class Article(PublishableModel):
    title = models.CharField(max_length=220, verbose_name="عنوان")
    slug = models.SlugField(max_length=240, unique=True, allow_unicode=True, verbose_name="نامک")
    excerpt = models.CharField(max_length=350, blank=True, verbose_name="خلاصه")
    body = models.TextField(verbose_name="متن")
    cover_image = models.ImageField(upload_to="articles/", blank=True, verbose_name="تصویر شاخص")
    published_at = models.DateTimeField(null=True, blank=True, db_index=True, verbose_name="زمان انتشار")
    is_demo = models.BooleanField(default=False, db_index=True, verbose_name="داده آزمایشی")

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title
