from django.urls import include, path
from rest_framework import routers

from .views import (
    CreateAccount,
    CustomerViewset,
    DriverRetriveUpdateView,
    DriverViewset,
    MyUserPasswordChange,
    MyUserViewset,
    SendOTP,
    UpdateDriverAvailabilityView,
)

router = routers.DefaultRouter()
router.register(r"admin/customers", CustomerViewset)
router.register(r"admin/drivers", DriverViewset)
router.register(r"admin/users", MyUserViewset)
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("user/changepassword/", MyUserPasswordChange.as_view()),
    path("getotp/", SendOTP.as_view()),
    path("update-account/", CreateAccount.as_view()),
    path(
        "driver/",
        DriverRetriveUpdateView.as_view(),
        name="update_driver",
    ),
    path(
        "driver/availability/",
        UpdateDriverAvailabilityView.as_view(),
        name="update_driver_availability",
    ),
    path("", include(router.urls)),
]
