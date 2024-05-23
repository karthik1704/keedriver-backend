from rest_framework import generics

from keedriver import permissions
from reviews.admin import ReviewAdmin
from .models import Review, Trip
from .serializers import ReviewCreateSerializer, ReviewSerialzer


class ReviewByTripId(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class=ReviewSerialzer
    permission_classes = {permissions.BasePermission}



class ReviewCreateTripId(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = {permissions.BasePermission}

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
   