from django.urls import include, path
from rest_framework import routers

from cars.views import CarViewSet

router = routers.DefaultRouter()
# router.register(r'triptypes', TripTypeViewset, basename='trips')
router.register(r"customer/cars", CarViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
]
