from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.core.models import PublishableModel
from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    lookup_field = "slug"
    queryset = Article.objects.filter(publication_status=PublishableModel.PublicationStatus.PUBLISHED)
