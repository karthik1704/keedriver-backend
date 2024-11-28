from drf_spectacular.utils import extend_schema
from rest_framework import generics

from keedriver import permissions

from .models import Review
from .serializers import ReviewCreateSerializer, ReviewSerialzer


@extend_schema(
    tags=["Reviews"],  # Add your custom tag here
)
class ReviewByTripId(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerialzer
    permission_classes = {permissions.BasePermission}


class ReviewCreateTripId(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = {permissions.BasePermission}

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
