from django.urls import include, path

from rest_framework import routers
from .views import TripViewset, TripTypeListView, TripTypeRDView,TripTypesCreate

router = routers.DefaultRouter()
# router.register(r'triptypes', TripTypeViewset, basename='trips')
router.register(r'trips', TripViewset)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('triptypes/', TripTypeListView.as_view()),
    path('triptypes/create/', TripTypesCreate.as_view()),
    path('triptypes/<int:pk>/', TripTypeRDView.as_view()),
    path('', include(router.urls)),
]
