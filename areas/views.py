from django.shortcuts import render

from rest_framework import viewsets, permissions

from .models import Area, City
from .serializers import AreaSerializer, CitySerializer
# Create your views here.

class AreaViewset(viewsets.ModelViewSet):
    
    queryset = Area.objects.all().order_by('-name')
    serializer_class = AreaSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]



class CityViewset(viewsets.ModelViewSet):
    
    queryset = City.objects.all().order_by('-name')
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
