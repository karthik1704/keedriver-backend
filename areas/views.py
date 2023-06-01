from django.shortcuts import render

from rest_framework import viewsets, permissions,filters
from django_filters.rest_framework import DjangoFilterBackend


from .models import Area, City
from .serializers import AreaSerializer, CitySerializer
# Create your views here.

class AreaViewset(viewsets.ModelViewSet):
    
    queryset = Area.objects.all().order_by('name')
    serializer_class = AreaSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
    filterset_fields = ['city']
    search_fields = ['name','city__name',  ]


class CityViewset(viewsets.ModelViewSet):
    
    queryset = City.objects.all().order_by('name')
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
    search_fields = ['name', ]


