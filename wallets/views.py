from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, permissions, status, viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from keedriver.permissions import IsDriver

from .models import DriverWallet, DriverWalletTransaction
from .serializers import DriverWalletSerializer, DriverWalletTransactionSerializer

# Create your views here.


@extend_schema(
    tags=["Admin Wallet"],  # Add your custom tag here
)
class AdminDriverWalletViewset(viewsets.ModelViewSet):

    queryset = DriverWallet.objects.all()
    serializer_class = DriverWalletSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = ["driver__first_name", "driver__phone"]
    search_fields = ["driver__first_name", "driver__phone"]

    class Meta:
        ordering = "-created_at"


@extend_schema(
    tags=["Admin Wallet"],  # Add your custom tag here
)
class AdminDriverWalletTransactionViewset(viewsets.ModelViewSet):

    queryset = DriverWalletTransaction.objects.all()
    serializer_class = DriverWalletTransactionSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = ["wallet__driver__first_name", "wallet__driver__phone"]
    search_fields = ["wallet__driver__first_name", "wallet__driver__phone"]

    class Meta:
        ordering = "-created_at"


@extend_schema(
    tags=["Driver Wallet"],  # Add your custom tag here
)
class DriverWalletViewset(RetrieveAPIView):

    queryset = DriverWallet.objects.none()
    serializer_class = DriverWalletSerializer
    permission_classes = [permissions.IsAuthenticated, IsDriver]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = ["driver__first_name", "driver__phone"]
    search_fields = ["driver__first_name", "driver__phone"]

    class Meta:
        ordering = "-created_at"

    def get_queryset(self):
        queryset = DriverWallet.objects.filter(driver=self.request.user)
        return queryset

    def get_object(self):
        return DriverWallet.objects.get(driver=self.request.user)


@extend_schema(
    tags=["Driver Wallet"],  # Add your custom tag here
)
class DriverWalletTransactionListAPIView(ListAPIView):

    queryset = DriverWalletTransaction.objects.all()
    serializer_class = DriverWalletTransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsDriver]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = ["wallet__driver__first_name", "wallet__driver__phone"]
    search_fields = ["wallet__driver__first_name", "wallet__driver__phone"]

    class Meta:
        ordering = "-id"

    def get_queryset(self):
        wallet = DriverWallet.objects.get(driver=self.request.user)
        queryset = DriverWalletTransaction.objects.filter(wallet=wallet).order_by("-id")
        return queryset


class IsWalletDriver(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(obj)
        print("hey")
        wallet = DriverWallet.objects.get(id=obj.wallet)
        return wallet.driver == request.user


@extend_schema(
    tags=["Driver Wallet"],  # Add your custom tag here
)
class DriverWalletTransactionDetailView(RetrieveAPIView):

    queryset = DriverWalletTransaction.objects.all()
    serializer_class = DriverWalletTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [
    #     DjangoFilterBackend,
    #     filters.SearchFilter,
    # ]
    # filterset_fields = ["wallet__driver__first_name", "wallet__driver__phone"]
    # search_fields = ["wallet__driver__first_name", "wallet__driver__phone"]

    class Meta:
        ordering = "-id"
