from django.urls import path
from .views import ConsultationCreateView, QuoteCreateView

urlpatterns = [
    path("consultations/", ConsultationCreateView.as_view(), name="consultation-create"),
    path("quotations/", QuoteCreateView.as_view(), name="quotation-create"),
]
