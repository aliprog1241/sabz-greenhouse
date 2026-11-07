import secrets
from decimal import Decimal
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from apps.core.models import TimeStampedModel
from apps.catalog.models import Product
from apps.services.models import Service

iran_phone_validator = RegexValidator(
    regex=r"^(?:\+98|0098|98|0)?9\d{9}$",
    message="شماره موبایل معتبر ایرانی وارد کنید.",
)

def generate_tracking_code():
    return f"SG-{secrets.token_hex(5).upper()}"

class LeadStatus(models.TextChoices):
    NEW = "NEW", "جدید"
    CONTACTED = "CONTACTED", "تماس گرفته‌شده"
    IN_PROGRESS = "IN_PROGRESS", "در حال پیگیری"
    CONVERTED = "CONVERTED", "تبدیل‌شده"
    CLOSED = "CLOSED", "بسته‌شده"

class LeadBase(TimeStampedModel):
    tracking_code = models.CharField(max_length=32, unique=True, default=generate_tracking_code,
                                     editable=False, verbose_name="کد پیگیری")
    full_name = models.CharField(max_length=150, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=16, validators=[iran_phone_validator], verbose_name="موبایل")
    province = models.CharField(max_length=100, verbose_name="استان")
    city = models.CharField(max_length=100, blank=True, verbose_name="شهر")
    status = models.CharField(max_length=16, choices=LeadStatus.choices, default=LeadStatus.NEW,
                              db_index=True, verbose_name="وضعیت")
    admin_notes = models.TextField(blank=True, verbose_name="یادداشت داخلی")

    class Meta:
        abstract = True

class ConsultationRequest(LeadBase):
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name="consultation_requests", verbose_name="خدمت")
    crop_type = models.CharField(max_length=150, verbose_name="نوع کشت")
    greenhouse_area = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))],
                                           verbose_name="مساحت گلخانه")
    cultivation_method = models.CharField(max_length=150, blank=True, verbose_name="روش کشت")
    problem_description = models.TextField(verbose_name="شرح مسئله")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "درخواست مشاوره"
        verbose_name_plural = "درخواست‌های مشاوره"

    def __str__(self):
        return f"{self.full_name} - {self.tracking_code}"

class QuoteRequest(LeadBase):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="quote_requests", verbose_name="محصول")
    product_name_snapshot = models.CharField(max_length=200, editable=False, verbose_name="نام محصول هنگام ثبت")
    unit_snapshot = models.CharField(max_length=50, editable=False, verbose_name="واحد هنگام ثبت")
    quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))],
                                   verbose_name="تعداد")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    privacy_accepted = models.BooleanField(verbose_name="پذیرش حریم خصوصی")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "درخواست استعلام"
        verbose_name_plural = "درخواست‌های استعلام"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.product_name_snapshot = self.product.name
            self.unit_snapshot = self.product.unit
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.product_name_snapshot} - {self.tracking_code}"
