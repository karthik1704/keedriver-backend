from os import read

import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, permissions, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from keedriver.permissions import IsDriver
from keedriver.utils import send_push_notification_to_user
from trips.models import DEDUCTION_PERCENTAGE, TRIP_STATUS, Trip
from trips.serializers import TripSerializer, TripStatusUpdateSerializer
from wallets.models import DriverWallet, DriverWalletTransaction


class TripFilter(django_filters.FilterSet):
    # Add a custom filter for excluding trips with a specific status
    trip_status_exclude = django_filters.MultipleChoiceFilter(
        field_name="trip_status",
        exclude=True,  # Exclude trips with the specified statuses
        choices=TRIP_STATUS,  # Assuming you have choices defined
    )
    trip_status_include = django_filters.MultipleChoiceFilter(
        field_name="trip_status",
        choices=TRIP_STATUS,  # Assuming you have choices defined
    )

    class Meta:
        model = Trip
        fields = [
            "trip_status",
            "amount_status",
            "trip_status_exclude",
            "trip_status_include",
        ]

    # def filter_trip_status_exclude(self, queryset, name, value):
    #     """
    #     Exclude trips with the specified trip_status.
    #     """
    #     statuses = value.split(",")  # Split the comma-separated list
    #     return queryset.exclude(trip_status__in=statuses)


@extend_schema(
    tags=["Driver Trips"],  # Add your custom tag here
)
class DriverTripViewset(viewsets.ModelViewSet):
    queryset = Trip.objects.none()
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated, IsDriver]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = TripFilter
    ordering_fields = [
        "trip_status",
    ]
    search_fields = ["trip_id", "customer__phone", "driver__phone"]

    def get_queryset(self):
        queryset = Trip.objects.filter(driver=self.request.user).order_by("-created_at")
        return queryset

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "POST operation is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "DELETE operation is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


@extend_schema(tags=["Driver Trips"])
class TripPaidAPIView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsDriver]
    queryset = Trip.objects.all()

    def get_object(self):
        trip_id = self.kwargs.get("pk")  # Get 'trip_id' from URL
        try:
            trip = Trip.objects.get(id=trip_id, driver=self.request.user)
        except Trip.DoesNotExist:
            raise NotFound(detail="Trip not found or unauthorized access.")
        return trip

    def update(self, request, *args, **kwargs):
        trip = self.get_object()
        if trip.trip_status != "COMPLETED":
            return Response(
                {"detail": "Trip already paid."},
                status=status.HTTP_409_CONFLICT,
            )
        if trip.amount_status == "PAID":
            return Response(
                {"detail": "Trip already paid."},
                status=status.HTTP_409_CONFLICT,
            )
        trip.amount_status = "PAID"
        trip.save(update_fields=["amount_status"])

        # wallet = DriverWallet.objects.get(driver=trip.driver)
        # if trip.amount is None:
        #     return Response(
        #         {"detail": "Trip amount is not set."},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )
        # deduction_amount = DEDUCTION_PERCENTAGE / 100 * trip.amount
        # remaing_amount = wallet.amount - deduction_amount
        # wallet.amount = remaing_amount
        # wallet.save()
        # DriverWalletTransaction.objects.create(
        #     wallet=wallet,
        #     trip=trip,
        #     transaction_type="DEDUCTION",
        #     amount=deduction_amount,
        # )

        return Response(
            {"detail": "Trip paid successfully."}, status=status.HTTP_200_OK
        )


@extend_schema(tags=["Driver Trips"])
class TripStatusUpdateAPIView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsDriver]
    queryset = Trip.objects.all()
    serializer_class = TripStatusUpdateSerializer

    def get_object(self):
        trip_id = self.kwargs.get("pk")  # Get 'trip_id' from URL
        print(trip_id)
        print(self.request.user)
        try:
            trip = Trip.objects.get(id=trip_id, driver=self.request.user)
        except Trip.DoesNotExist:
            raise NotFound(detail="Trip not found or unauthorized access.")
        return trip

    def update(self, request, *args, **kwargs):
        trip = self.get_object()
        trip_status = request.data.get("trip_status")

        # Check if trip is already completed
        if trip.trip_status == "COMPLETED":
            return Response(
                {"detail": "Trip already completed."},
                status=status.HTTP_409_CONFLICT,
            )

        # Validate and save the updated trip_status using the serializer
        serializer = self.get_serializer(
            trip, data={"trip_status": trip_status}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        send_push_notification_to_user(
            request.user, "Trip Updated", f"Trip status updated to {trip_status}"
        )

        return Response(
            {"detail": f"Trip status updated to '{trip_status}' successfully."},
            status=status.HTTP_200_OK,
        )
