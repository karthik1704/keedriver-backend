from django.urls import include, path
from rest_framework import routers

from hire_us.views import HireReportCreateView, HireReportRetrieveView, HireUsViewSet

router = routers.DefaultRouter()

router.register(r"hire", HireUsViewSet, basename="hire_us")


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "hire/report/create/", HireReportCreateView.as_view(), name="hire-report-create"
    ),
    path(
        "hire/report/<int:id>/",
        HireReportRetrieveView.as_view(),
        name="hire-detail-view",
    ),
]
