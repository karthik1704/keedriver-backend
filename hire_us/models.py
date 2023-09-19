from django.db import models
from django.forms import ValidationError
from django.utils import timezone

from accounts.models import Customer, Driver
from areas.models import Area

# Create your models here.

PAYMENT_STATUS = [("NOT PAID", "Not Paid"), ("PAID", "Paid")]
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
    amount_status = models.CharField(
        choices=PAYMENT_STATUS, default="NOT PAID", max_length=150
    )

    total_amount = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True
    )
    trip_status = models.CharField(choices=TRIP_STATUS, max_length=25, default="ACTIVE")

    # Inculuding and excluding saturday and sunday
    include_saturday = models.BooleanField(default=False)
    include_sunday = models.BooleanField(default=False)

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
    trip_status = models.CharField(choices=HIRE_TRIP_STATUS, default="DRAFT")
    trip_start_time = models.TimeField(blank=True, null=True)
    trip_end_time = models.TimeField(blank=True, null=True)
    trip_hours = models.DurationField(default=timezone.timedelta(hours=2), null=True)


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
        choices=PAYMENT_STATUS, default="NOT PAID", max_length=150
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
        print(trips)
        date_invoiced = []
        for trip in trips:
            if trip.trip_status == "INVOICED":
                date_invoiced.append(trip.trip_date)
        print(date_invoiced)
        if date_invoiced:
            print("HI")
            raise ValidationError(
                f'These date already invoiced {",".join(map(str, date_invoiced))}'
            )

        return super().clean()


class DriverReport(models.Model):
    report = models.ForeignKey(HireusReport, on_delete=models.CASCADE)
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
    report = models.ForeignKey(HireusReport, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.DO_NOTHING)
    trip_id = models.ForeignKey(HireTrips, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.driver.get_full_name()
