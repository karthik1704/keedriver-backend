from django.urls import include, path
from rest_framework import routers

from .views.admins import (
    DashboardCustomerChartView,
    DashboardView,
    TripTypeListView,
    TripTypeRDView,
    TripTypesCreate,
    TripTypeUpdateView,
    TripViewset,
)
from .views.customers import CustomerTripViewset
from .views.drivers import DriverTripViewset, TripPaidAPIView, TripStatusUpdateAPIView

router = routers.DefaultRouter()
# router.register(r'triptypes', TripTypeViewset, basename='trips')
router.register(r"trips", TripViewset)
router.register(r"customer/trips", CustomerTripViewset, basename="customer_trips")
router.register(r"driver/trips", DriverTripViewset, basename="driver_trips")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("triptypes/", TripTypeListView.as_view()),
    path("triptypes/create/", TripTypesCreate.as_view()),
    path("triptypes/<int:pk>/", TripTypeRDView.as_view()),
    path("triptypes/update/<int:pk>/", TripTypeUpdateView.as_view()),
    path("dashboard/", DashboardView.as_view()),
    path("dashboard/customer/", DashboardCustomerChartView.as_view()),
    path("trip-status/<int:pk>/", TripStatusUpdateAPIView.as_view()),
    path("trip-paid/<int:pk>/", TripPaidAPIView.as_view()),
    path("", include(router.urls)),
]
