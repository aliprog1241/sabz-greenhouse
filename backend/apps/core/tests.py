from rest_framework import status
from rest_framework.test import APISimpleTestCase
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from .admin import SiteSettingsAdmin
from .models import SiteSettings


class HealthCheckTests(APISimpleTestCase):
    def test_health_endpoint(self):
        response = self.client.get("/api/v1/health/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "ok")

    def test_openapi_schema_is_available(self):
        response = self.client.get("/api/schema/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SiteSettingsAdminTests(TestCase):
    def setUp(self):
        self.model_admin = SiteSettingsAdmin(SiteSettings, admin.site)
        self.request = RequestFactory().get("/admin/")
        self.request.user = get_user_model().objects.create_superuser(
            username="settings-admin", email="settings@example.com", password="test-pass"
        )

    def test_settings_are_singleton_and_cannot_be_deleted(self):
        self.assertTrue(self.model_admin.has_add_permission(self.request))
        settings = SiteSettings.objects.create()
        self.assertFalse(self.model_admin.has_add_permission(self.request))
        self.assertFalse(self.model_admin.has_delete_permission(self.request, settings))
