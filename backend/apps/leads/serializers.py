from rest_framework import serializers
from apps.catalog.models import Product
from apps.core.models import PublishableModel
from apps.services.models import Service
from .models import ConsultationRequest, QuoteRequest


class AntiSpamMixin:
    def validate(self, attrs):
        if attrs.pop("website", ""):
            raise serializers.ValidationError({"non_field_errors": ["درخواست نامعتبر است."]})
        return super().validate(attrs)


class ConsultationRequestSerializer(AntiSpamMixin, serializers.ModelSerializer):
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        source="service",
        queryset=Service.objects.filter(publication_status=PublishableModel.PublicationStatus.PUBLISHED),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = ConsultationRequest
        fields = ("full_name", "phone", "province", "city", "crop_type", "greenhouse_area",
                  "service_id", "problem_description", "cultivation_method", "website")


class QuoteRequestSerializer(AntiSpamMixin, serializers.ModelSerializer):
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source="product",
        queryset=Product.objects.filter(
            is_active=True,
            publication_status=PublishableModel.PublicationStatus.PUBLISHED,
        ),
    )

    class Meta:
        model = QuoteRequest
        fields = ("product_id", "full_name", "phone", "province", "city", "quantity",
                  "description", "privacy_accepted", "website")

    def validate_privacy_accepted(self, value):
        if value is not True:
            raise serializers.ValidationError("پذیرش حریم خصوصی الزامی است.")
        return value


class SubmissionResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    tracking_code = serializers.CharField()
    status = serializers.CharField()
