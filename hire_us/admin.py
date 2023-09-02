from django.contrib import admin

from .models import HireUs, HireTrips

# Register your models here.
class HireTripsInline(admin.StackedInline):
    model=HireTrips


class HireUsAdmin(admin.ModelAdmin):
    pass

admin.site.register(HireUs)