from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.core.models import PublishableModel
from .models import Service
from .serializers import ServiceSerializer

class ServiceViewSet(ReadOnlyModelViewSet):
    serializer_class = ServiceSerializer
    lookup_field = "slug"
    queryset = Service.objects.filter(publication_status=PublishableModel.PublicationStatus.PUBLISHED)
