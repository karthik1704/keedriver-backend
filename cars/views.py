from typing import Generic
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView


from cars.models import Car
from cars.models import CarType
from cars.models import CarEngineType
from cars.serializers import CarCreateSerializer, CarDeleteSerializer, CarEngineTypeSerializer, CarSerializer, CarTypeSerializer,CarReadSerializer,CarUpdateSerializer
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
    permission_classes = { permissions.IsAuthenticated,IsCustomer}

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class CarUpdateSView(UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarUpdateSerializer
    permission_classes = {permissions.IsAuthenticated}



class CarDeleteView(DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarDeleteSerializer
    permission_classes = [permissions.IsAuthenticated]





class CarReadView(RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]


class CarGentric(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]

class CarTypeGentric(generics.ListAPIView):
    queryset = CarType.objects.all()
    serializer_class = CarTypeSerializer
    permission_classes = [permissions.AllowAny]

class CarEngineTypeGentric(generics.ListAPIView):
    queryset = CarEngineType.objects.all()
    serializer_class = CarEngineTypeSerializer
    permission_classes =[permissions.AllowAny]


    
