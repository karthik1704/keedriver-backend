from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from .models import DriverWallet, DriverWalletTransaction


@receiver(post_save, sender=DriverWalletTransaction)
def add_trip_id(sender, instance, created, **kwargs):
    if created:
        if instance.transaction_type == 'ADD':
            wallet = DriverWallet.objects.get(pk=instance.wallet.pk)
            sum_amount = instance.amount + wallet.amount
            wallet.amount = sum_amount
            wallet.save()

    

