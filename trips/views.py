from django.shortcuts import render
from dal import autocomplete
from accounts.models import Driver
from django.db.models import Q
from django.db.models import Case, When

# Create your views here.


class DriverAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Driver.objects.none()

        qs = Driver.objects.all()

        area = self.forwarded.get("pickup_area", None)
        by_location = self.forwarded.get("driver_based_on_loaction", None)
        print(self.q)
        if by_location:
            if area:
                # qs = qs.order_by( Case(When(driverprofile__area__in=area, then=0), default=1))
                qs = qs.filter(driverprofile__area__in=area).order_by("first_name")
        else:
            qs = Driver.objects.all()

        if self.q:
            qs = qs.filter(
                Q(first_name__istartswith=self.q) | Q(phone__contains=self.q)
            )

        return qs
