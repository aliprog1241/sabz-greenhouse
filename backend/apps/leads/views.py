from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import (
    ConsultationRequestSerializer,
    QuoteRequestSerializer,
    SubmissionResponseSerializer,
)


class SubmissionCreateView(generics.CreateAPIView):
    response_serializer_class = SubmissionResponseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response = {"success": True, "tracking_code": instance.tracking_code, "status": instance.status}
        return Response(response, status=status.HTTP_201_CREATED)


@extend_schema(responses={201: SubmissionResponseSerializer})
class ConsultationCreateView(SubmissionCreateView):
    serializer_class = ConsultationRequestSerializer
    throttle_scope = "consultation"


@extend_schema(responses={201: SubmissionResponseSerializer})
class QuoteCreateView(SubmissionCreateView):
    serializer_class = QuoteRequestSerializer
    throttle_scope = "quotation"
