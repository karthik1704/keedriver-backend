from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from .models import Trip

from wallets.models import DriverWallet


@receiver(post_save, sender=Trip)
def add_Trip_id(sender, instance, created, **kwargs):
    if created:
        year = timezone.now().strftime("%Y")
        id = str(instance.id)
        trip_id = f"KD{year}{id}"
        instance.trip_id=trip_id
        instance.save()


