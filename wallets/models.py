from django.db import models

from accounts.models import Driver
from trips.models import Trip

# Create your models here.


class DriverWallet(models.Model):
    driver = models.OneToOneField(Driver, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=19, decimal_places=2)

    def __str__(self) -> str:
        return self.driver.get_full_name()


TRANSACTION_TYPE = (
    ("ADD", "ADD MONEY"),
    ("DEDUCTION", "Deduction"),
)

# updated_amount = models.DecimalField(max_digits=19, decimal_places=2)
class DriverWalletTransaction(models.Model):
    wallet = models.ForeignKey(DriverWallet, on_delete=models.DO_NOTHING)
    trip = models.ForeignKey(Trip, on_delete=models.DO_NOTHING, null=True, blank=True)
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, max_length=20)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    

    transaction_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.wallet.driver.get_full_name()
