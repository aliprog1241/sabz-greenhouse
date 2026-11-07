from django.db import IntegrityError, transaction
from django.test import TestCase
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
