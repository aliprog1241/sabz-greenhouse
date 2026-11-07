from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from .models import Certificate, PublishableModel
from .serializers import CertificateSerializer

@extend_schema(responses=inline_serializer(
    name="HealthResponse",
    fields={"status": serializers.CharField(), "service": serializers.CharField()},
))
@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "service": "sabz-greenhouse-api"})

class CertificateListView(generics.ListAPIView):
    serializer_class = CertificateSerializer
    pagination_class = None
    queryset = Certificate.objects.filter(publication_status=PublishableModel.PublicationStatus.PUBLISHED)

