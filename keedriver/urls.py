"""keedriver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from trips.views.admins import DriverAutocomplete, TripTypeAutocomplete

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


admin.site.site_header = "Kee Driver "
admin.site.site_title = "Kee Driver Dashboard"
admin.site.index_title = "Kee Driver Admin"

urlpatterns = [
    re_path(
        r"^driver-autocomplete/$",
        DriverAutocomplete.as_view(),
        name="driver-autocomplete",
    ),
    re_path(
        r"^triptype-autocomplete/$",
        TripTypeAutocomplete.as_view(),
        name="triptype-autocomplete",
    ),
    path("admin/", admin.site.urls),
    path("api/v1/rest/", include("rest_framework.urls")),
    path("api/v1/", include("dj_rest_auth.urls")),
    path("api/v1/", include("accounts.urls")),
    path("api/v1/", include("areas.urls")),
    path("api/v1/", include("trips.urls")),
    path("api/v1/", include("wallets.urls")),
    # YOUR PATTERNS
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


