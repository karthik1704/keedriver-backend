from django.urls import include, path
from rest_framework import routers

# from cars.views import CarViewSet
from cars.views import (
    CarCreateListView,
    CarEngineTypeGentric,
    CarTypeGentric,
    CarUpdateRetriveView,
)

# router = routers.DefaultRouter()
# # router.register(r'triptypes', TripTypeViewset, basename='trips')
# router.register(r"customer/cars", CarViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("cars/", CarCreateListView.as_view()),
    path("cars/<int:pk>/", CarUpdateRetriveView.as_view()),
    path("cartype/", CarTypeGentric.as_view()),
    path("carenginetype/", CarEngineTypeGentric.as_view()),
]
