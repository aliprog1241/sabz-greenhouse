from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.core.models import PublishableModel
from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer
    lookup_field = "slug"
    queryset = Project.objects.filter(
        publication_status=PublishableModel.PublicationStatus.PUBLISHED
    ).prefetch_related("images")
