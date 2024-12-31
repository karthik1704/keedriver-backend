from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, permissions, viewsets

from .models import Area, City
from .serializers import AreaSerializer, CitySerializer


# Create your views here.
@extend_schema(
    tags=["Area"],  # Add your custom tag here
)
class AreaViewset(viewsets.ModelViewSet):

    queryset = Area.objects.all().order_by("name")
    serializer_class = AreaSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = ["city"]
    search_fields = [
        "name",
        "city__name",
    ]


@extend_schema(
    tags=["Cities"],  # Add your custom tag here
)
class CityViewset(viewsets.ModelViewSet):

    queryset = City.objects.all().order_by("name")
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    search_fields = [
        "name",
    ]
