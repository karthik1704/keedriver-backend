from django.db import models

from accounts.models import Customer

# Create your models here.

transmission_types = (("AUTO", "Automatic"), ("MANUAL", "Manual"))


class CarType(models.Model):
    type_name = models.CharField(max_length=50)


class CarEngineType(models.Model):
    engine_type = models.CharField(max_length=100)


class Car(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=25)
    transmission_type = models.CharField(
        choices=transmission_types, default="AUTO", max_length=15
    )
    type = models.ForeignKey(CarType, on_delete=models.DO_NOTHING, null=True)

    engine_model = models.ForeignKey(
        CarEngineType, on_delete=models.DO_NOTHING, null=True
    )

    def __str__(self) -> str:
        return self.model
