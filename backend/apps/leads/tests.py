from django.test import TestCase
from apps.catalog.models import Category, Product
from .models import QuoteRequest

class QuoteRequestModelTests(TestCase):
    def test_product_snapshot_is_created_server_side(self):
        category = Category.objects.create(name="تجهیزات", slug="equipment")
        product = Product.objects.create(category=category, name="فن گلخانه", slug="fan", unit="دستگاه")
        quote = QuoteRequest.objects.create(
            product=product, full_name="کاربر آزمایشی", phone="09121234567", province="تهران",
            quantity=2, privacy_accepted=True,
        )
        self.assertEqual(quote.product_name_snapshot, "فن گلخانه")
        self.assertEqual(quote.unit_snapshot, "دستگاه")
        self.assertTrue(quote.tracking_code.startswith("SG-"))
