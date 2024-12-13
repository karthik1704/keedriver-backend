from os import read

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, permissions, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from keedriver.permissions import IsDriver
from trips.models import DEDUCTION_PERCENTAGE, Trip
from trips.serializers import TripSerializer
from wallets.models import DriverWallet, DriverWalletTransaction


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
    filterset_fields = ["trip_status", "amount_status"]
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
    serializer_class = TripSerializer(read_only=True)

    def get_object(self):
        trip_id = self.kwargs.get("trip_id")  # Access 'trip_id' from URL
        try:
            trip = Trip.objects.get(trip_id=trip_id, driver=self.request.user)
        except Trip.DoesNotExist:
            raise NotFound(detail="Trip not found or unauthorized access.")
        return trip

    def update(self, request):
        trip = Trip.objects.get(trip_id=request.data.get("trip_id"))
        if trip.amount_status == "PAID":
            return Response(
                {"detail": "Trip already paid."},
                status=status.HTTP_200_OK,
            )
        trip.amount_status = "PAID"
        trip.save()
        if trip.amount_status == "PAID":
            wallet = DriverWallet.objects.get(driver=trip.driver)
            if trip.amount is None:
                return Response(
                    {"detail": "Trip amount is not set."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            deduction_amount = DEDUCTION_PERCENTAGE / 100 * trip.amount
            print(deduction_amount)
            remaing_amount = wallet.amount - deduction_amount
            wallet.amount = remaing_amount
            wallet.save()
            wallet_transaction = DriverWalletTransaction.objects.create(
                wallet=wallet,
                trip=trip,
                transaction_type="DEDUCTION",
                amount=deduction_amount,
            )
            wallet_transaction.save()

        return Response(
            {"detail": "Trip paid successfully."}, status=status.HTTP_200_OK
        )


@extend_schema(tags=["Driver Trips"])
class TripCompleteAPIView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsDriver]
    queryset = Trip.objects.all()
    serializer_class = TripSerializer(read_only=True)

    def get_object(self):
        trip_id = self.kwargs.get("trip_id")  # Access 'trip_id' from URL
        try:
            trip = Trip.objects.get(trip_id=trip_id, driver=self.request.user)
        except Trip.DoesNotExist:
            raise NotFound(detail="Trip not found or unauthorized access.")
        return trip

    def update(self, request, *args, **kwargs):
        trip = self.get_object()
        if trip.trip_status == "COMPLETED":
            return Response(
                {"detail": "Trip already completed."},
                status=status.HTTP_200_OK,
            )
        trip.trip_status = "COMPLETED"
        trip.save()
        return Response(
            {"detail": "Trip completed successfully."},
            status=status.HTTP_200_OK,
        )
