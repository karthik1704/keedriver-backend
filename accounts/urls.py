from django.urls import include, path
from rest_framework import routers
from .views import CustomerViewset, DriverViewset, MyUserViewset

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewset)
router.register(r'drivers', DriverViewset)
router.register(r'users', MyUserViewset)
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
