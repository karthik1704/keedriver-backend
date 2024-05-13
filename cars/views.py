from msilib.schema import ListView
from typing import Generic
from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework import generics

from cars.models import Car
from cars.models import CarType
from cars.models import CarEngineType
from cars.serializers import CarEngineTypeSerializer, CarSerializer, CarTypeSerializer
from keedriver.permissions import IsCustomer


# Create your views here.
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.none()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return Car.objects.filter(customer=self.request.user)
    
class CarTypeGentric(generics.ListAPIView):
    queryset = CarType.objects.all()
    serializer_class = CarTypeSerializer
    permission_classes = [permissions.AllowAny]

class CarEngineTypeGentric(generics.ListAPIView):
    queryset = CarEngineType.objects.all()
    serializer_class = CarEngineTypeSerializer
    permission_classes =[permissions.AllowAny]


    
