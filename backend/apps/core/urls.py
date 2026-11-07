from django.urls import path
from .views import CertificateListView, health
urlpatterns = [
    path("health/", health, name="health"),
    path("certificates/", CertificateListView.as_view(), name="certificate-list"),
]

