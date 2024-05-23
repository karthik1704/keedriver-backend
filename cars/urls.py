from django.urls import include, path
from rest_framework import routers

# from cars.views import CarViewSet
from cars.views import CarCreateView, CarReadView, CreateAPIView
from cars.views import CarTypeGentric,CarGentric
from cars.views import CarEngineTypeGentric

# router = routers.DefaultRouter()
# # router.register(r'triptypes', TripTypeViewset, basename='trips')
# router.register(r"customer/cars", CarViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path("", include(router.urls)),
    path ("car/",CarGentric.as_view()),
    path("car/create/", CarCreateView.as_view()),
    path("cartype/", CarTypeGentric.as_view()),
    path ("carenginetype/", CarEngineTypeGentric.as_view()),
    path("car/<int:pk>/",CarReadView.as_view())
    
]
