from rest_framework import generics, permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from cars.models import Car, CarEngineType, CarType
from cars.serializers import CarEngineTypeSerializer, CarSerializer, CarTypeSerializer
from keedriver.permissions import IsCustomer


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


class CarUpdateRetriveView(RetrieveUpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = {permissions.IsAuthenticated, IsCustomer}


# class CarReadView(RetrieveAPIView):
#     queryset = Car.objects.none()
#     serializer_class = CarReadSerializer
#     permission_classes = {
#         permissions.AllowAny,
#     }

#     def get_queryset(self):
#         return Car.objects.filter(customer=self.request.user)


class CarGentric(generics.ListAPIView):
    queryset = Car.objects.none()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return Car.objects.filter(customer=self.request.user)


class CarTypeGentric(generics.ListAPIView):
    queryset = CarType.objects.all()
    serializer_class = CarTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class CarEngineTypeGentric(generics.ListAPIView):
    queryset = CarEngineType.objects.all()
    serializer_class = CarEngineTypeSerializer
    permission_classes = [permissions.AllowAny]
