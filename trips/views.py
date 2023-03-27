from django.shortcuts import render
from dal import autocomplete
from django.db.models import Q
from django.db.models import Case, When
from rest_framework import viewsets, permissions, filters
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend


from accounts.models import Driver
from .models import Trip,TripType
from .serializers import TripTypeSerializer,  TripTypeCreateSerializer, TripSerializer

# Create your views here.


class TripTypeListView(GenericAPIView, ListModelMixin, ):
    queryset = TripType.objects.all()
    serializer_class = TripTypeSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        q= TripType.objects.filter(depth=1).order_by('id')
        for type in q:
            type.children = type.get_children()
        return q
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class TripTypeRDView(GenericAPIView, RetrieveModelMixin, DestroyModelMixin,UpdateModelMixin ):
    queryset = TripType.objects.all().order_by('-id')
    serializer_class = TripTypeSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]



    def get(self, request,  *args, **kwargs):
       
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request,  *args, **kwargs):
       
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TripTypesCreate(GenericAPIView, CreateModelMixin):
    queryset = TripType.objects.all()
    serializer_class = TripTypeCreateSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def post(self, request,  *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class TripViewset(viewsets.ModelViewSet):
    
    queryset = Trip.objects.all().order_by('trip_status')
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["trip_status", "amount_status"]
    ordering_fields = ["trip_status", ]
    search_fields = ['trip_id', 'customer__phone',  'driver__phone']


class DriverAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Driver.objects.none()

        qs = Driver.objects.all()

        area = self.forwarded.get("pickup_area", None)
        by_location = self.forwarded.get("driver_based_on_loaction", None)
        if by_location:
            if area:
                # qs = qs.order_by( Case(When(driverprofile__area__in=area, then=0), default=1))
                qs = qs.filter(driverprofile__area__in=area).order_by("first_name")
        else:
            qs = Driver.objects.all().order_by("first_name")

        if self.q:
            qs = qs.filter(
                Q(first_name__istartswith=self.q) | Q(phone__contains=self.q)
            ).order_by("first_name")

        return qs



class TripTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return TripType.objects.none()

        qs = Driver.objects.none()

        parent = self.forwarded.get("trip_parent_type", None)
       
        if parent:
            obj = TripType.objects.get(pk=parent).get_children().order_by("name")    
            print(obj)
            qs = obj 
            if self.q:
                qs = qs.filter(
                    Q(name__istartswith=self.q)
                )

        return qs
