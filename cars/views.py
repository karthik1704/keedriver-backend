from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from cars.models import Car, CarEngineType, CarType
from cars.serializers import CarEngineTypeSerializer, CarSerializer, CarTypeSerializer
from keedriver.permissions import IsCustomer


@extend_schema(
    tags=["Cars"],  # Add your custom tag here
)
class CarCreateListView(ListCreateAPIView):

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    # Handle GET request (list)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # Handle POST request (create)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # Customize creation behavior
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(customer=self.request.user)


@extend_schema(
    tags=["Cars"],  # Add your custom tag here
)
class CarUpdateRetriveView(RetrieveUpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = {permissions.IsAuthenticated, IsCustomer}


@extend_schema(
    tags=["Cars"],  # Add your custom tag here
)
class CarTypeGentric(generics.ListAPIView):
    queryset = CarType.objects.all()
    serializer_class = CarTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    tags=["Cars"],  # Add your custom tag here
)
class CarEngineTypeGentric(generics.ListAPIView):
    queryset = CarEngineType.objects.all()
    serializer_class = CarEngineTypeSerializer
    permission_classes = [permissions.AllowAny]
