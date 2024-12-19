from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from keedriver import permissions
from trips.models import Trip

from .models import Review
from .serializers import ReviewCreateSerializer, ReviewSerialzer


@extend_schema(
    tags=["Reviews"],  # Add your custom tag here
)
class ReviewByTripId(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerialzer
    permission_classes = {permissions.IsCustomer, IsAuthenticated}

    def get_queryset(self):
        trip_id = self.kwargs.get("trip_id")  # Get 'trip_id' from URL
        print(trip_id)
        reviews = Review.objects.filter(
            trip=trip_id, reviewer=self.request.user
        ).order_by("-id")
        return reviews


@extend_schema(
    tags=["Reviews"],  # Add your custom tag here
)
class CreateReview(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated, permissions.IsCustomer]

    def perform_create(self, serializer):
        trip = serializer.validated_data.get("trip")

        # Save the review with additional fields
        serializer.save(reviewer=self.request.user, review_to=trip.driver)
