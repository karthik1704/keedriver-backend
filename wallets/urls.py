from django.urls import include, path
from rest_framework import routers
from .views import (
    AdminDriverWalletViewset,
    AdminDriverWalletTransactionViewset,
    DriverWalletViewset,
    DriverWalletTransactionViewset,
)

router = routers.DefaultRouter()
router.register(r"wallets", AdminDriverWalletViewset)
router.register(r"wallettransactions", AdminDriverWalletTransactionViewset)
router.register(r"driver/wallet", DriverWalletViewset)
router.register(r"driver/wallet/transactions", DriverWalletTransactionViewset)
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
]
