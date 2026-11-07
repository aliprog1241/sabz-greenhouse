from rest_framework import filters, generics
from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from apps.core.models import PublishableModel
from .models import Category, Product
from .serializers import CategorySerializer, ProductDetailSerializer, ProductListSerializer

class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = None
    queryset = Category.objects.filter(is_active=True).select_related("parent")

@extend_schema_view(list=extend_schema(parameters=[
    OpenApiParameter(name="category", type=str, location=OpenApiParameter.QUERY,
                     description="نامک دسته‌بندی محصول"),
]))
class ProductViewSet(ReadOnlyModelViewSet):
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "brand", "sku", "description")

    def get_queryset(self):
        queryset = Product.objects.filter(
            is_active=True,
            publication_status=PublishableModel.PublicationStatus.PUBLISHED,
        ).select_related("category").prefetch_related("images")
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset

    def get_serializer_class(self):
        return ProductDetailSerializer if self.action == "retrieve" else ProductListSerializer
