from django.db import models
from apps.core.models import PublishableModel, TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=150, verbose_name="نام")
    slug = models.SlugField(max_length=170, unique=True, allow_unicode=True, verbose_name="نامک")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT,
                               related_name="children", verbose_name="دسته والد")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="فعال")

    class Meta:
        ordering = ["name"]
        verbose_name = "دسته محصول"
        verbose_name_plural = "دسته‌های محصول"

    def __str__(self):
        return self.name


class Product(PublishableModel):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", verbose_name="دسته")
    name = models.CharField(max_length=200, verbose_name="نام")
    slug = models.SlugField(max_length=220, unique=True, allow_unicode=True, verbose_name="نامک")
    sku = models.CharField(max_length=80, unique=True, null=True, blank=True, verbose_name="SKU")
    brand = models.CharField(max_length=150, blank=True, verbose_name="برند")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    specifications = models.JSONField(default=dict, blank=True, verbose_name="مشخصات فنی")
    unit = models.CharField(max_length=50, verbose_name="واحد")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="فعال")
    is_featured = models.BooleanField(default=False, db_index=True, verbose_name="ویژه")

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["category", "is_active"])]
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="محصول")
    image = models.ImageField(upload_to="products/", verbose_name="تصویر")
    alt_text = models.CharField(max_length=250, verbose_name="متن جایگزین")
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="ترتیب")

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصول"

    def __str__(self):
        return f"{self.product} - {self.sort_order}"
