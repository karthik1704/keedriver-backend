from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify


from treebeard.mp_tree import MP_Node
from django.utils.safestring import mark_safe
from accounts.models import Customer, Driver

# Create your models here.
class TripType(MP_Node):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    node_order_by = ["name"]

    def __str__(self):
        return "Category: {}".format(self.name)


    def save(self, *args, **kwargs) -> None:
        if not self.slug or self.slug != self.name:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


# CHOICES = MoveNodeForm.mk_dropdown_tree(Category)
# category = ChoiceField(choices=CHOICES)


class TripDeatil(models.Model):
    pickup = models.CharField(max_length=255)


class Trip(models.Model):

    PAYMENT_STATUS = [("NOT PAID", "Not Paid"), ("PAID", "Paid")]
    TRIP_STATUS = [
        ("ACTIVE", "Active"),
        ("COMPELETED", "Compeleted"),
        ("CANCELLED", "Cancelled"),
    ]

    customer = models.ForeignKey(
        Customer, related_name="customer", on_delete=models.DO_NOTHING
    )
    driver = models.ForeignKey(
        Driver, related_name="driver", on_delete=models.DO_NOTHING
    )
    trip_type = models.ForeignKey(TripType, on_delete=models.DO_NOTHING)
    trip_status = models.CharField(choices=TRIP_STATUS, max_length=25, default="ACTIVE")

    pickup_location = models.CharField(max_length=255)
    pickup_time = models.DateTimeField()
    drop_location = models.CharField(max_length=255, blank=True, null=True)
    drop_time = models.DateTimeField( blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)

    amount = models.DecimalField(max_digits=19, decimal_places=4)
    amount_status = models.CharField(
        choices=PAYMENT_STATUS, default="NOT PAID", max_length=150
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.first_name


# new Model
class Trip1(models.Model):

    customer = models.ForeignKey(
        Customer, related_name="customer1", on_delete=models.DO_NOTHING
    )

    trip_type = models.ForeignKey(TripType, on_delete=models.DO_NOTHING)
    pickup_location = models.CharField(max_length=255)
    pickup_time = models.DateTimeField()
    drop_location = models.CharField(max_length=255, blank=True, null=True)

    amount = models.DecimalField(max_digits=19, decimal_places=4)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.first_name


class AssignDriver(models.Model):
    trip = models.ForeignKey(Trip1, on_delete=models.CASCADE)
    driver = models.ForeignKey(
        Driver, related_name="driver1", on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.trip.customer.first_name


class AssignCar(models.Model):
    pass


class Payment(models.Model):
    PAYMENT_MODE = [("OFFINE", "OFFINE"), ("ONLINE", "ONLINE")]
    # PAYMENT_TYPE = [('Pay on car', "Pay on car"),( "UPI",  "UPI")]
    PAYMENT_STATUS = [("NOT PAID", "Not Paid"), ("PAID", "Paid")]

    trip = models.ForeignKey(Trip1, on_delete=models.CASCADE)
    payment_status = models.CharField(
        choices=PAYMENT_STATUS, default="NOT PAID", max_length=150
    )

    def __str__(self):
        return self.trip.customer.first_name
