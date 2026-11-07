from django.test import TestCase
from apps.catalog.models import Category, Product
from apps.core.models import PublishableModel
from apps.services.models import Service
from .models import QuoteRequest
from .models import ConsultationRequest
from rest_framework.test import APITestCase
from django.core.cache import cache
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from .admin import QuoteRequestAdmin

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


class LeadSubmissionApiTests(APITestCase):
    def setUp(self):
        cache.clear()
        category = Category.objects.create(name="تجهیزات", slug="equipment")
        self.product = Product.objects.create(
            category=category, name="فن گلخانه", slug="fan", unit="دستگاه",
            publication_status=PublishableModel.PublicationStatus.PUBLISHED,
        )
        self.service = Service.objects.create(
            title="مشاوره کشت", slug="crop-consulting", description="مشاوره تخصصی",
            publication_status=PublishableModel.PublicationStatus.PUBLISHED,
        )

    def quote_payload(self, **overrides):
        payload = {
            "product_id": self.product.id,
            "full_name": "کاربر آزمایشی",
            "phone": "09121234567",
            "province": "تهران",
            "city": "تهران",
            "quantity": "2.00",
            "description": "نیاز به پیش‌فاکتور",
            "privacy_accepted": True,
        }
        payload.update(overrides)
        return payload

    def test_quote_submission_returns_only_tracking_contract(self):
        response = self.client.post("/api/v1/quotations/", self.quote_payload(), format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(set(response.data), {"success", "tracking_code", "status"})
        quote = QuoteRequest.objects.get(tracking_code=response.data["tracking_code"])
        self.assertEqual(quote.product_name_snapshot, self.product.name)
        self.assertNotIn("phone", response.data)

    def test_quote_rejects_missing_privacy_and_honeypot(self):
        privacy_response = self.client.post(
            "/api/v1/quotations/", self.quote_payload(privacy_accepted=False), format="json"
        )
        spam_response = self.client.post(
            "/api/v1/quotations/", self.quote_payload(website="https://spam.invalid"), format="json"
        )
        self.assertEqual(privacy_response.status_code, 400)
        self.assertEqual(spam_response.status_code, 400)

    def test_consultation_submission(self):
        response = self.client.post("/api/v1/consultations/", {
            "service_id": self.service.id,
            "full_name": "گلخانه‌دار آزمایشی",
            "phone": "09121234567",
            "province": "فارس",
            "city": "شیراز",
            "crop_type": "گوجه‌فرنگی",
            "greenhouse_area": "1200.00",
            "cultivation_method": "هیدروپونیک",
            "problem_description": "بررسی شرایط کشت",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(ConsultationRequest.objects.filter(tracking_code=response.data["tracking_code"]).exists())

    def test_quote_rate_limit(self):
        responses = [
            self.client.post("/api/v1/quotations/", self.quote_payload(), format="json")
            for _ in range(11)
        ]
        self.assertTrue(all(response.status_code == 201 for response in responses[:10]))
        self.assertEqual(responses[10].status_code, 429)


class LeadAdminTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="تجهیزات", slug="admin-equipment")
        product = Product.objects.create(
            category=category, name="فن مدیریتی", slug="admin-fan", unit="دستگاه"
        )
        self.quote = QuoteRequest.objects.create(
            product=product,
            full_name="کاربر پنل",
            phone="09121234567",
            province="تهران",
            quantity=1,
            privacy_accepted=True,
        )
        self.model_admin = QuoteRequestAdmin(QuoteRequest, admin.site)
        self.request = RequestFactory().get("/admin/")
        self.request.user = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="test-pass"
        )

    def test_submitted_leads_cannot_be_added_or_deleted_in_admin(self):
        self.assertFalse(self.model_admin.has_add_permission(self.request))
        self.assertFalse(self.model_admin.has_delete_permission(self.request, self.quote))

    def test_only_status_and_internal_notes_are_editable_after_submission(self):
        readonly = self.model_admin.get_readonly_fields(self.request, self.quote)

        self.assertIn("phone", readonly)
        self.assertIn("product", readonly)
        self.assertNotIn("status", readonly)
        self.assertNotIn("admin_notes", readonly)
