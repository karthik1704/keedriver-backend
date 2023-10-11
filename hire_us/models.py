from __future__ import annotations

from collections.abc import Iterable
from decimal import Decimal

from django.db import models
from django.forms import ValidationError
from django.utils import timezone

from accounts.models import Customer, Driver
from areas.models import Area

# Create your models here.

PAYMENT_STATUS = [("DRAFT", "Draft"), ("NOT PAID", "Not Paid"), ("PAID", "Paid")]
TRIP_STATUS = [
    ("ACTIVE", "Active"),
    ("COMPLETED", "Completed"),
    ("CANCELLED", "Cancelled"),
]
HIRE_TRIP_STATUS = [
    ("DRAFT", "Draft"),
    ("INPROCESS", "Inprocess"),
    ("COMPLETED", "Completed"),
    ("INVOICED", "Invoiced"),
    ("CANCELLED", "Cancelled"),
]


class HireUs(models.Model):
    hire_id = models.CharField(
        unique=True,
        editable=False,
        max_length=250,
    )

    customer = models.ForeignKey(
        Customer, related_name="hcustomer", on_delete=models.DO_NOTHING
    )

    driver = models.ForeignKey(
        Driver,
        related_name="hmdriver",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    pickup_area = models.ForeignKey(Area, on_delete=models.DO_NOTHING)
    pickup_location = models.CharField(max_length=255, blank=True, null=True)
    drop_location = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()

    report_time = models.TimeField(
        blank=True,
        null=True,
    )
    end_time = models.TimeField(
        blank=True,
        null=True,
    )

    alternate_phone_number = models.CharField(max_length=39, blank=True, null=True)

    amount_per_day = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True
    )

    trip_status = models.CharField(choices=TRIP_STATUS, max_length=25, default="ACTIVE")

    # Including and excluding saturday and sunday
    include_saturday = models.BooleanField(default=False)
    include_sunday = models.BooleanField(default=False)

    driver_cut_percentage = models.DecimalField(
        max_digits=4, decimal_places=2, default=Decimal(10.00)
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hire us"
        verbose_name_plural = "Hire us"

    def __str__(self):
        return f"{self.hire_id} - {self.customer.get_full_name()}"


class HireTrips(models.Model):
    hire = models.ForeignKey(
        HireUs, on_delete=models.CASCADE, related_name="hire_trips"
    )
    driver = models.ForeignKey(
        Driver,
        related_name="hdriver",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    trip_date = models.DateField(default=timezone.now)
    trip_status = models.CharField(
        choices=HIRE_TRIP_STATUS, default="DRAFT", blank=True, null=True
    )
    trip_start_time = models.TimeField(blank=True, null=True)
    trip_end_time = models.TimeField(blank=True, null=True)
    trip_hours = models.DurationField(
        default=timezone.timedelta(hours=0), null=True, blank=True
    )

    def __str__(self) -> str:
        return ""

    class Meta:
        verbose_name = "Hire Trip"
        verbose_name_plural = "Hire Trips"

    def save(
        self,
        force_insert: bool = ...,
        force_update: bool = ...,
        using: str | None = ...,
        update_fields: Iterable[str] | None = ...,
    ) -> None:
        if self.trip_start_time and self.trip_end_time:
            start_time = self.trip_start_time
            end_time = self.trip_end_time
            start_time_sec = (
                start_time.hour * 3600 + start_time.minute * 60 + start_time.second
            )
            end_time_sec = end_time.hour * 3600 + end_time.minute * 60 + end_time.second
            hours = end_time_sec - start_time_sec
            self.trip_hours = timezone.timedelta(seconds=hours)

        return super().save()


class HireusReport(models.Model):
    hire = models.ForeignKey(HireUs, on_delete=models.DO_NOTHING)
    report_title = models.CharField(max_length=255)
    billing_start_date = models.DateField()
    billing_end_date = models.DateField()
    trip_count = models.IntegerField()
    trip_attended = models.IntegerField()
    amount_per_day = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True
    )
    total_amount = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True
    )
    amount_status = models.CharField(
        choices=PAYMENT_STATUS, default="DRAFT", max_length=150
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.report_title

    def clean(self) -> None:
        start_date = self.billing_start_date
        end_date = self.billing_end_date
        trips = self.hire.hire_trips.filter(  # type:ignore
            trip_date__gte=start_date, trip_date__lte=end_date
        )
        trip_count = trips.count()
        date_invoiced = []
        date_processing = []
        date_draft = []
        for trip in trips:
            if trip.trip_status == "INVOICED":
                date_invoiced.append(trip.trip_date)
            if trip.trip_status == "INPROCESS":
                date_processing.append(trip.trip_date)
            if trip.trip_status == "DRAFT":
                date_draft.append(trip.trip_date)

        if self.amount_status == "DRAFT":
            if trip_count == 0:
                raise ValidationError(f"No trips found in between dates")
            if date_invoiced:
                raise ValidationError(
                    f'These date already invoiced {",".join(map(str, date_invoiced))}'
                )
            if date_processing:
                raise ValidationError(
                    f"""These date still InProcess - please update the date or change date  
                    {",".join(map(str, date_processing))}"""
                )
            if date_draft:
                raise ValidationError(
                    f"""These date still Draft - please update the date or change date  
                    {",".join(map(str, date_draft))}"""
                )
        return super().clean()


class DriverReport(models.Model):
    report = models.ForeignKey(
        HireusReport, related_name="driver_report", on_delete=models.CASCADE
    )
    driver = models.ForeignKey(Driver, on_delete=models.DO_NOTHING)
    total_working_hours = models.DurationField()
    driver_trip_count = models.IntegerField()
    driver_amount = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.driver.get_full_name()


class HireTripReport(models.Model):
    report = models.ForeignKey(
        HireusReport, related_name="hire_trip_report", on_delete=models.CASCADE
    )
    trip_id = models.ForeignKey(HireTrips, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return ""


class HirePaymentReport(models.Model):
    hire_report = models.ForeignKey(
        HireusReport, related_name="payment_report", on_delete=models.CASCADE
    )
    hire_amount = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True
    )
    total_driver_amount = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True
    )
    remaining_amount = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"Payment report of {self.hire_report.report_title}"
