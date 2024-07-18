from django.urls import include, path
from rest_framework import routers

from .views import (
    AdminDriverWalletTransactionViewset,
    AdminDriverWalletViewset,
    DriverWalletTransactionViewset,
    DriverWalletViewset,
)

router = routers.DefaultRouter()
router.register(r"wallets", AdminDriverWalletViewset)
router.register(r"wallettransactions", AdminDriverWalletTransactionViewset)
router.register(r"driver/wallet", DriverWalletViewset, basename="driver_wallet")
router.register(
    r"driver/wallet/transactions",
    DriverWalletTransactionViewset,
    basename="driver_wallet_transaction",
)
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
]
