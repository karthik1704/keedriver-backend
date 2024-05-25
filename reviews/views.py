from tkinter import NO
from rest_framework import generics

from rest_framework import permissions
from trips.models import Trip

from .models import Review
from .serializers import ReviewCreateSerializer, ReviewSerialzer,ReviewPutSerializer,ReviewDeleteSerialize


class ReviewByTripId(generics.ListAPIView):
    
    serializer_class=ReviewSerialzer
    permission_classes = {permissions.IsAuthenticated}
    

    def get_queryset(self):
        trip_id = self.kwargs['trip_id']
        return Review.objects.filter(reviewer=self.request.user, trip=trip_id)
        

        

class ReviewCreateTripId(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = {permissions.IsAuthenticated}

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

class ReviewPutTrip(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewPutSerializer
    permission_classes ={permissions.IsAuthenticated}

class ReviewDeleteTrip(generics.DestroyAPIView):
    queryset= Review.objects.all()
    serializer_class = ReviewDeleteSerialize
    permission_classes ={permissions.IsAuthenticated}

   