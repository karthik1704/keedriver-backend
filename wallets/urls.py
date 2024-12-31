from django.urls import include, path
from rest_framework import routers

from .views import (
    AdminDriverWalletTransactionViewset,
    AdminDriverWalletViewset,
    DriverWalletTransactionDetailView,
    DriverWalletTransactionListAPIView,
    DriverWalletViewset,
)

router = routers.DefaultRouter()
router.register(r"wallets", AdminDriverWalletViewset)
router.register(r"wallettransactions", AdminDriverWalletTransactionViewset)
# router.register(r"driver/wallet", DriverWalletViewset, basename="driver_wallet")
# router.register(
#     r"driver/wallet/transactions",
#     DriverWalletTransactionViewset,
#     basename="driver_wallet_transaction",
# )
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("driver/wallet", DriverWalletViewset.as_view(), name="driver_wallet"),
    path(
        "driver/wallet/transactions",
        DriverWalletTransactionListAPIView.as_view(),
        name="driver_wallet",
    ),
    path(
        "driver/wallet/transactions/<int:pk>",
        DriverWalletTransactionDetailView.as_view(),
        name="driver_wallet",
    ),
    path("", include(router.urls)),
]
