from django.shortcuts import render
from rest_framework import permissions, viewsets

from cars.models import Car
from cars.serializers import CarSerializer
from keedriver.permissions import IsCustomer


# Create your views here.
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.none()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return Car.objects.filter(customer=self.request.user)
