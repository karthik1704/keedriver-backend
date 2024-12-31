from django.urls import include, path
from rest_framework import routers

from .views import (
    CustomerCreateReview,
    CustomerReviewByTripId,
    DriverCreateReview,
    DriverReviewByTripId,
    ReviewViewset,
)

router = routers.DefaultRouter()
# router.register(r'triptypes', TripTypeViewset, basename='trips')
router.register(r"review/admin", ReviewViewset)

urlpatterns = [
    path("review/customer/create/", CustomerCreateReview.as_view()),
    path("review/driver/create/", DriverCreateReview.as_view()),
    path("review/customer/<int:trip_id>/", CustomerReviewByTripId.as_view()),
    path("review/driver/<int:trip_id>/", DriverReviewByTripId.as_view()),
    path("", include(router.urls)),
]
