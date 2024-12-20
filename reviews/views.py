from drf_spectacular.utils import extend_schema
from rest_framework import generics, viewsets
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from trips.models import Trip

from .models import Review
from .serializers import ReviewCreateSerializer, ReviewSerialzer


class IsCustomer(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        # Assuming `request.user` has a `is_driver` attribute or similar
        return hasattr(request.user, "is_customer") and request.user.is_customer

    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user


class IsDriver(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        # Assuming `request.user` has a `is_driver` attribute or similar
        return hasattr(request.user, "is_driver") and request.user.is_driver

    def has_object_permission(self, request, view, obj):
        print(obj.reviewer)
        return obj.reviewer == request.user


@extend_schema(
    tags=["Reviews"],  # Add your custom tag here
)
class CustomerReviewByTripId(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerialzer
    permission_classes = [IsCustomer, IsAuthenticated]

    def get_queryset(self):
        trip_id = self.kwargs.get("trip_id")  # Get 'trip_id' from URL
        reviews = Review.objects.filter(
            trip=trip_id, reviewer=self.request.user
        ).order_by("-id")
        return reviews


@extend_schema(
    tags=["Reviews"],  # Add your custom tag here
)
class DriverReviewByTripId(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerialzer
    permission_classes = [IsAuthenticated, IsDriver]

    def get_queryset(self):
        trip_id = self.kwargs.get("trip_id")  # Get 'trip_id' from URL

        reviews = Review.objects.filter(
            trip=trip_id, reviewer=self.request.user
        ).order_by("-id")
        return reviews


@extend_schema(
    tags=["Reviews"],  # Add your custom tag here
)
class CustomerCreateReview(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def perform_create(self, serializer):
        trip = serializer.validated_data.get("trip")
        print(trip.trip_status)
        if trip.trip_status != "COMPLETED":
            Response({"message": "Trip not completed"})
        # Save the review with additional fields
        serializer.save(reviewer=self.request.user, review_to=trip.driver)


@extend_schema(
    tags=["Reviews"],  # Add your custom tag here
)
class DriverCreateReview(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def perform_create(self, serializer):
        trip = serializer.validated_data.get("trip")

        # Save the review with additional fields
        serializer.save(reviewer=self.request.user, review_to=trip.customer)


@extend_schema(
    tags=["Admin Reviews"],  # Add your custom tag here
)
class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
