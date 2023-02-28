from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from .models import Trip, DEDUCTION_PERCENTAGE
from wallets.models import DriverWallet, DriverWalletTransaction


@receiver(post_save, sender=Trip)
def add_trip_id(sender, instance, created, **kwargs):
    if created:
        year = instance.created_at.strftime("%Y")
        id = str(instance.id)
        trip_id = f"KD{year}{id}"
        instance.trip_id = trip_id
        instance.save()

    if not created:
        updated = kwargs.get("update_fields")
        print(updated)
        if updated and "amount_status" in updated:
            if instance.amount_status == "PAID":
                wallet = DriverWallet.objects.get(driver=instance.driver)
                deduction_amount = DEDUCTION_PERCENTAGE / 100 * instance.amount
                print(deduction_amount)
                remaing_amount = wallet.amount - deduction_amount
                wallet.amount = remaing_amount
                wallet.save()
                wallet_transaction = DriverWalletTransaction.objects.create(
                    wallet=wallet,
                    trip=instance,
                    transaction_type="DEDUCTION",
                    amount=deduction_amount,
                )
                wallet_transaction.save()
                instance.save()


# @receiver(post_save, sender=Trip)
# def driver_amount_deduction(sender, instance, created,  **kwargs):

#     updated = kwargs['update_fields']
#     print(updated)


# if 'amount_status' in updated:
#     if instance.amount_status == 'PAID':
#         wallet =  DriverWallet.objects.get(driver = instance.driver)
#         deduction_amount = DEDUCTION_PERCENTAGE / 100 * instance.amount
#         print(deduction_amount)
#         print(deduction_amount - wallet.amount)
#         instance.save()
