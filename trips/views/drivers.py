


from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend


from keedriver.permissions import IsDriver 

from trips.models import Trip
from trips.serializers import TripSerializer

class DriverTripViewset(viewsets.ModelViewSet):
    queryset = Trip.objects.none()
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated, IsDriver]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["trip_status", "amount_status"]
    ordering_fields = [
        "trip_status",
    ]
    search_fields = ["trip_id", "customer__phone", "driver__phone"]

    def get_queryset(self):
        queryset = Trip.objects.filter(driver=self.request.user)
        return queryset