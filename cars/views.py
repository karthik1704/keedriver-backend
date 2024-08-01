from typing import Generic

from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView

from cars.models import Car, CarEngineType, CarType
from cars.serializers import (
    CarCreateSerializer,
    CarEngineTypeSerializer,
    CarReadSerializer,
    CarSerializer,
    CarTypeSerializer,
)
from keedriver.permissions import IsCustomer
from trips.views import customers

# Create your views here.
# class CarViewSet(viewsets.ModelViewSet):
#     queryset = Car.objects.none()
#     serializer_class = CarSerializer
#     permission_classes = [permissions.IsAuthenticated, IsCustomer]
#     def get_queryset(self):
#         return Car.objects.filter(customer=self.request.user)


class CarCreateView(CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarCreateSerializer
    permission_classes = {permissions.IsAuthenticated, IsCustomer}

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class CarUpdateView(UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarCreateSerializer
    permission_classes = {permissions.IsAuthenticated, IsCustomer}


class CarReadView(RetrieveAPIView):
    queryset = Car.objects.none()
    serializer_class = CarReadSerializer
    permission_classes = {
        permissions.AllowAny,
    }

    def get_queryset(self):
        return Car.objects.filter(customer=self.request.user)


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
