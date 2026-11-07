from django.core.exceptions import ValidationError
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین ویرایش")

    class Meta:
        abstract = True


class PublishableModel(TimeStampedModel):
    class PublicationStatus(models.TextChoices):
        DRAFT = "DRAFT", "پیش‌نویس"
        PUBLISHED = "PUBLISHED", "منتشرشده"

    publication_status = models.CharField(
        max_length=12,
        choices=PublicationStatus.choices,
        default=PublicationStatus.DRAFT,
        db_index=True,
        verbose_name="وضعیت انتشار",
    )

    class Meta:
        abstract = True


class SiteSettings(TimeStampedModel):
    site_name = models.CharField(max_length=150, default="Sabz Greenhouse", verbose_name="نام سایت")
    specialist_name = models.CharField(max_length=150, default="امیررضا قشنی", verbose_name="نام متخصص")
    phone = models.CharField(max_length=20, blank=True, verbose_name="تلفن")
    email = models.EmailField(blank=True, verbose_name="ایمیل")
    address = models.TextField(blank=True, verbose_name="نشانی")
    about = models.TextField(blank=True, verbose_name="درباره مجموعه")

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def clean(self):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError("فقط یک رکورد تنظیمات سایت مجاز است.")

    def __str__(self):
        return self.site_name


class Certificate(PublishableModel):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    issuer = models.CharField(max_length=200, blank=True, verbose_name="صادرکننده")
    issued_on = models.DateField(null=True, blank=True, verbose_name="تاریخ صدور")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    image = models.ImageField(upload_to="certificates/", blank=True, verbose_name="تصویر")
    is_demo = models.BooleanField(default=False, db_index=True, verbose_name="داده آزمایشی")

    class Meta:
        ordering = ["-issued_on", "title"]
        verbose_name = "گواهی"
        verbose_name_plural = "گواهی‌ها"

    def __str__(self):
        return self.title
