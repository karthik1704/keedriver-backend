from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.viewsets import ModelViewSet

from hire_us.models import HireUs
from hire_us.serializers import HireUsReportSerializer, HireUsSerializer

# Create your views here.


class HireUsViewSet(ModelViewSet):
    serializer_class = HireUsSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        return self.model.objects.all()


class HireReportCreateView(CreateAPIView):
    serializer_class = HireUsReportSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        return self.model.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        start_date = serializer.validated_data.get("billing_start_date")
        end_date = serializer.validated_data.get("billing_end_date")
        hire_id = serializer.validated_data.get("hire")

        hire = HireUs.objects.get(pk=hire_id.id)

        if hire:
            trip_count = hire.hire_trips.filter(trip_date__gte=start_date, trip_date__lte=end_date).count() | 0  # type: ignore
            trip_attended = hire.hire_trips.filter(trip_date__gte=start_date, trip_date__lte=end_date, trip_status="COMPLETED").count()  # type: ignore
            amount_per_day = hire.amount_per_day
            total_amount = trip_attended * amount_per_day
            serializer.save(
                trip_count=trip_count,
                trip_attended=trip_attended,
                amount_per_day=amount_per_day,
                total_amount=total_amount,
            )
        return super().perform_create(serializer)


class HireReportRetrieveView(RetrieveAPIView):
    serializer_class = HireUsReportSerializer
    model = serializer_class.Meta.model
    lookup_field = "id"

    def get_queryset(self):
        return self.model.objects.all()
