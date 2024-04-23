from __future__ import annotations

import calendar
from datetime import date, timedelta

import django_filters
from dal import autocomplete
from django.db import models as django_models
from django.db.models import Case, Count, Q, Sum, When
from django.db.models.functions import TruncDate, TruncDay, TruncMonth
from django.shortcuts import render
from django.utils.timezone import datetime, localdate, make_aware, timedelta
from django_filters import rest_framework as drfilters
from django_filters import widgets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Customer, Driver
from keedriver.permissions import IsCustomer, IsDriver
from trips.models import Trip, TripType
from trips.serializers import (
    TripDashboardSerializer,
    TripSerializer,
    TripTypeCreateSerializer,
    TripTypeDetailSerializer,
    TripTypeSerializer,
    TripTypeUpdateSerializer,
)

# Create your views here.


class TripTypeListView(
    GenericAPIView,
    ListModelMixin,
):
    queryset = TripType.objects.all()
    serializer_class = TripTypeSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        q = TripType.objects.filter(depth=1).order_by("id")
        for type in q:
            type.children = type.get_children()
        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TripTypeRDView(
    GenericAPIView,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
):
    queryset = TripType.objects.all().order_by("-id")
    serializer_class = TripTypeDetailSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.children = instance.get_children()
            instance.parent = instance.get_parent()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TripTypeUpdateView(
    GenericAPIView,
    UpdateModelMixin,
):
    queryset = TripType.objects.all().order_by("-id")
    serializer_class = TripTypeUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    permission_classes = [permissions.AllowAny]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        parent_id = serializer.validated_data.get("parent_id")
        print(serializer.validated_data)
        print(parent_id)
        if parent_id:
            parent = TripType.objects.get(pk=parent_id)
            print(parent)
            print(instance)
            instance.move(parent, pos=None)
            instance.save()
            instance.refresh_from_db()
            instance.get_root()
            print(instance.get_root())
        self.perform_update(serializer)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class TripTypesCreate(GenericAPIView, CreateModelMixin):
    queryset = TripType.objects.all()
    serializer_class = TripTypeCreateSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TripFilter(drfilters.FilterSet):
    class Meta:
        model = Trip
        fields = {
            "trip_status": ["exact"],
            "amount_status": ["exact"],
            "created_at": ["gte", "lte", "exact"],
        }

    filter_overrides = {
        django_models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},
    }


class TripViewset(viewsets.ModelViewSet):
    queryset = Trip.objects.all().order_by("trip_status")
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    # filterset_fields = {
    #     "trip_status": ["exact"],
    #     "amount_status": ["exact"],
    #     "created_at": ["gte", "lte", "exact",],
    # }
    filterset_class = TripFilter
    ordering_fields = [
        "trip_status",
    ]
    search_fields = ["trip_id", "customer__phone", "driver__phone"]


class DriverAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Driver.objects.none()

        customer = self.forwarded.get("customer", None)

        block_ids = list(
            Customer.objects.get(pk=customer)
            .blocked_by.all()  # type: ignore
            .values_list("blocked_user", flat=True)
        )
        print(block_ids)
        qs = (
            Driver.objects.exclude(pk__in=block_ids)
            .filter(
                driverprofile__license_expiry_date__gte=date.today()
                + timedelta(days=10)
            )
            .order_by("first_name")
        )

        area = self.forwarded.get("pickup_area", None)
        by_location = self.forwarded.get("driver_based_on_loaction", None)
        pickup_time = self.forwarded.get("pickup_time", None)

        # print(pickup_time)
        # if pickup_time:
        #     pickup_date = pickup_time.date()
        #     print(pickup_date)

        if by_location:
            if area:
                # qs = qs.order_by( Case(When(driverprofile__area__in=area, then=0), default=1))
                qs = qs.filter(driverprofile__area__in=area).order_by("first_name")
        else:
            qs = (
                Driver.objects.exclude(pk__in=block_ids)
                .filter(
                    driverprofile__license_expiry_date__gte=date.today()
                    + timedelta(days=10)
                )
                .order_by("first_name")
            )

        if self.q:
            qs = qs.filter(
                Q(first_name__istartswith=self.q) | Q(phone__contains=self.q)
            ).order_by("first_name")

        return qs


class TripTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return TripType.objects.none()

        qs = TripType.objects.none()

        parent = self.forwarded.get("trip_parent_type", None)

        if parent:
            obj = TripType.objects.get(pk=parent).get_children().order_by("-id")
            print(obj)
            qs = obj
            if self.q:
                qs = qs.filter(Q(name__istartswith=self.q))

        return qs


class DashboardView(APIView):
    serializer_class = TripDashboardSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get(self, request, format=None):
        today = make_aware(datetime.now())

        today_trips = Trip.objects.filter(
            created_at__year=today.year,
            created_at__month=today.month,
            created_at__day=today.day,
        ).count()

        last_30_days_trips = Trip.objects.filter(
            created_at__lte=today,
            created_at__gt=today - timedelta(days=30),
        ).count()

        trip_active = Trip.objects.filter(trip_status="ACTIVE").count()
        trip_completed = Trip.objects.filter(trip_status="COMPLETED").count()

        total_trips = Trip.objects.all().count()
        cancelled_trips = Trip.objects.filter(trip_status="CANCELLED").count()

        today_amount = Trip.objects.filter(
            amount_status="PAID",
            created_at__year=today.year,
            created_at__month=today.month,
            created_at__day=today.day,
        ).aggregate(Sum("amount"))["amount__sum"]

        today_amount = today_amount if today_amount is not None else 0

        last_30_days_amount = Trip.objects.filter(
            amount_status="PAID",
            created_at__lte=today,
            created_at__gt=today - timedelta(days=30),
        ).aggregate(Sum("amount"))["amount__sum"]

        last_30_days_amount = (
            last_30_days_amount if last_30_days_amount is not None else 0
        )

        total_amount = Trip.objects.all().aggregate(Sum("amount"))["amount__sum"]
        total_amount_paid = Trip.objects.filter(
            amount_status="PAID",
        ).aggregate(
            Sum("amount")
        )["amount__sum"]
        pending_amount = Trip.objects.filter(amount_status="NOT PAID").aggregate(
            Sum("amount")
        )["amount__sum"]

        pending_amount = pending_amount if pending_amount is not None else 0

        total_drivers = Driver.objects.all().count()
        active_drivers = Driver.objects.filter(is_active=True).count()
        today_joined_drivers = (
            Driver.objects.filter(
                date_joined__year=today.year,
                date_joined__month=today.month,
                date_joined__day=today.day,
            ).count()
            | 0
        )

        trips_lines = (
            Trip.objects.filter(
                created_at__lte=today,
                created_at__gt=today - timedelta(days=30),
            )
            .annotate(
                day=TruncDate("created_at")
            )  # Truncate to month and add to select list
            .values("day")  # Group By month
            .annotate(count=Count("id"))  # Select the count of the grouping
            .order_by("-day")
        )

        return Response(
            {
                "trips": {
                    "today": today_trips,
                    "30days": last_30_days_trips,
                    "total_trips": total_trips,
                    "active_trips": trip_active,
                    "trip_completed": trip_completed,
                    "cancelled_trips": cancelled_trips,
                },
                "amount": {
                    "today": today_amount,
                    "30days": last_30_days_amount,
                    "total_amount": total_amount,
                    "total_amount_paid": total_amount_paid,
                    "pending_amount": pending_amount,
                },
                "drivers": {
                    "total": total_drivers,
                    "active": active_drivers,
                    "today": today_joined_drivers,
                },
                "trips_line": trips_lines,
            }
        )


class DashboardCustomerChartView(APIView):
    def get(self, request, format=None):
        users = Customer.objects.all()
        months = []
        for user in users:
            months.append(user.date_joined.date().month)
        months = list(set(months))
        months.sort()
        data = []
        for month in months:
            data.append(
                {
                    "month": calendar.month_name[month],
                    "count": Customer.objects.filter(date_joined__month=month).count(),
                }
            )
        return Response(data, status=status.HTTP_200_OK)


# trips : {
# today : 10,
# 30days : 100
# },
# active_trips : 10
# amount : {
# today : 300,
# 30days : 10000
# },
# drivers : {
# total : 50,
# active : 48,
# today : 4
# },
# trips_line :{
# 05/06 : 10,
# 04/06 :8,
# 03/06 : 12
# ...
# ...
# 06/05 : 15
# }
