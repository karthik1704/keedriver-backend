from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from keedriver.permissions import IsCustomer
from trips.models import Trip
from trips.serializers import CustomerTripSerializer, TripSerializer


class CustomerTripViewset(viewsets.ModelViewSet):
    queryset = Trip.objects.none()
    serializer_class = CustomerTripSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
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
        queryset = Trip.objects.filter(customer=self.request.user)
        return queryset
