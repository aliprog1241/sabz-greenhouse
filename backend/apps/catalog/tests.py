from django.db import IntegrityError, transaction
from django.test import TestCase
from rest_framework.test import APITestCase
from apps.core.models import PublishableModel
from .models import Category, Product

class CatalogModelTests(TestCase):
    def test_category_slug_is_unique(self):
        Category.objects.create(name="تجهیزات", slug="equipment")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Category.objects.create(name="تجهیزات دیگر", slug="equipment")

    def test_product_string_representation(self):
        category = Category.objects.create(name="تجهیزات", slug="equipment")
        product = Product.objects.create(category=category, name="فن گلخانه", slug="fan", unit="دستگاه")
        self.assertEqual(str(product), "فن گلخانه")


class ProductApiTests(APITestCase):
    def setUp(self):
        self.irrigation = Category.objects.create(name="آبیاری", slug="irrigation")
        self.ventilation = Category.objects.create(name="تهویه", slug="ventilation")
        Product.objects.create(
            category=self.irrigation, name="پمپ آبیاری", slug="water-pump", unit="دستگاه",
            brand="سبز", publication_status=PublishableModel.PublicationStatus.PUBLISHED,
        )
        Product.objects.create(
            category=self.ventilation, name="فن گلخانه", slug="greenhouse-fan", unit="دستگاه",
            publication_status=PublishableModel.PublicationStatus.PUBLISHED,
        )
        Product.objects.create(category=self.irrigation, name="محصول پیش‌نویس", slug="draft", unit="عدد")

    def test_list_excludes_drafts_and_supports_search(self):
        response = self.client.get("/api/v1/products/", {"search": "پمپ"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["slug"], "water-pump")

    def test_category_slug_filter(self):
        response = self.client.get("/api/v1/products/", {"category": "ventilation"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["slug"] for item in response.data["results"]], ["greenhouse-fan"])
