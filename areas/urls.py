from django.urls import include, path
from rest_framework import routers
from .views import AreaViewset, CityViewset

router = routers.DefaultRouter()
router.register(r'areas', AreaViewset)
router.register(r'cities', CityViewset)
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
