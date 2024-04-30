import decimal

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe
from location_field.models.plain import PlainLocationField
from treebeard.mp_tree import MP_Node

from accounts.models import Customer, Driver, MyUser
from areas.models import Area
from cars.models import Car


# Create your models here.
class TripType(MP_Node):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    node_order_by = ["name"]

    def __str__(self):
        # return "%s%s" % ("" if self.depth == 1 else "--" * self.depth, self.name)
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug or self.slug != self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# CHOICES = MoveNodeForm.mk_dropdown_tree(Category)
# category = ChoiceField(choices=CHOICES)


PAYMENT_STATUS = [("NOT PAID", "Not Paid"), ("PAID", "Paid")]
TRIP_STATUS = [
    ("ACTIVE", "Active"),
    ("COMPLETED", "Completed"),
    ("CANCELLED", "Cancelled"),
]

DEDUCTION_PERCENTAGE = decimal.Decimal(10.00)


class Trip(models.Model):
    # Trip id "KD" prefix ,follow by current year and trip primary key
    trip_id = models.CharField(
        unique=True,
        editable=False,
        max_length=250,
    )
    customer = models.ForeignKey(
        Customer, related_name="customer", on_delete=models.DO_NOTHING
    )
    driver = models.ForeignKey(
        Driver,
        related_name="driver",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING, blank=True, null=True)
    alternate_phone_number = models.CharField(max_length=39, blank=True, null=True)
    trip_type = models.ForeignKey(TripType, on_delete=models.DO_NOTHING)
    trip_status = models.CharField(choices=TRIP_STATUS, max_length=25, default="ACTIVE")

    pickup_area = models.ForeignKey(Area, on_delete=models.DO_NOTHING)
    pickup_location = models.CharField(max_length=255, blank=True, null=True)

    pickup_time = models.DateTimeField(blank=True, null=True)
    drop_location = models.CharField(max_length=255, blank=True, null=True)
    drop_time = models.DateTimeField(blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)

    amount = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    amount_status = models.CharField(
        choices=PAYMENT_STATUS, default="NOT PAID", max_length=150
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trip_id} - {self.customer.get_full_name()}"
