from django.db import models

from accounts.models import Driver, Customer
from areas.models import Area

# Create your models here.

PAYMENT_STATUS = [("NOT PAID", "Not Paid"), ("PAID", "Paid")]
TRIP_STATUS = [
    ("ACTIVE", "Active"),
    ("COMPLETED", "Completed"),
    ("CANCELLED", "Cancelled"),
]


class HireUs(models.Model):
    hire_id = models.CharField(
        unique=True,
        editable=False,
        max_length=250,
    )

    customer = models.ForeignKey(
        Customer, related_name="customer", on_delete=models.DO_NOTHING
    )

    alternate_phone_number = models.CharField(max_length=39, blank=True, null=True)

    pickup_area = models.ForeignKey(Area, on_delete=models.DO_NOTHING)
    pickup_location = models.CharField(max_length=255, blank=True, null=True)

    pickup_time = models.DateTimeField(blank=True, null=True)
    drop_location = models.CharField(max_length=255, blank=True, null=True)
    drop_time = models.DateTimeField(blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hire_id} - {self.customer.get_full_name()}"


class HireTrips(models.Model):
    hire = models.ForeignKey(HireUs, on_delete=models.CASCADE)
    driver = models.ForeignKey(
        Driver,
        related_name="driver",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    trip_date = models.DateTimeField()
    trip_status = models.BooleanField(default=False)
