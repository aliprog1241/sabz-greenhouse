from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/", include("apps.core.urls")),
    path("api/v1/", include("apps.catalog.urls")),
    path("api/v1/", include("apps.services.urls")),
    path("api/v1/", include("apps.projects.urls")),
    path("api/v1/", include("apps.blog.urls")),
    path("api/v1/", include("apps.leads.urls")),
]

admin.site.site_header = "مدیریت سبز گلخانه"
admin.site.site_title = "سبز گلخانه"
admin.site.index_title = "مدیریت محتوا و درخواست‌ها"

