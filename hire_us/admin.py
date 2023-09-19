from typing import Any

from django.contrib import admin
from django.http.request import HttpRequest
from django.utils import timezone

from accounts.models import Driver
from trips.models import DEDUCTION_PERCENTAGE

from .models import DriverReport, HireTripReport, HireTrips, HireUs, HireusReport


# Register your models here.
class HireTripsInline(admin.TabularInline):
    model = HireTrips
    extra = 0
    classes = ("collapse",)

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)
        if formfield:
            formfield.widget.can_delete_related = False  # type: ignore
            formfield.widget.can_change_related = False  # type: ignore
            # formfield.widget.can_add_related = False  # can change this, too
            # formfield.widget.can_view_related = False  # can change this, too

        return formfield

    def get_readonly_fields(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> list[str] | tuple[Any, ...]:
        if obj:
            return ("trip_date",)
        return super().get_readonly_fields(request, obj)


class HireUsAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "hire_id",
        "pickup_location",
        "drop_location",
        "start_date",
        "end_date",
    )
    inlines = (HireTripsInline,)
    fieldsets = (
        (
            "Customer Information",
            {
                "fields": (
                    "customer",
                    "alternate_phone_number",
                ),
            },
        ),
        (
            "Trip Information",
            {
                "fields": (
                    "pickup_area",
                    "pickup_location",
                    "drop_location",
                    "start_date",
                    "end_date",
                    "include_saturday",
                    "include_sunday",
                ),
            },
        ),
        (
            "Report Timing",
            {
                "fields": (
                    "report_time",
                    "end_time",
                ),
            },
        ),
        (
            "Driver Information",
            {
                "fields": ("driver",),
            },
        ),
        (
            "Amount Information",
            {
                "fields": (
                    "amount_per_day",
                    "total_amount",
                ),
            },
        ),
        (
            "Status",
            {
                "fields": ("trip_status",),
            },
        ),
    )

    def get_inlines(self, request, obj=None):
        if obj:
            return [HireTripsInline]
        else:
            return []

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)

        formfield.widget.can_delete_related = False  # type: ignore
        formfield.widget.can_change_related = False  # type: ignore
        # formfield.widget.can_add_related = False  # can change this, too
        # formfield.widget.can_view_related = False  # can change this, too

        return formfield


class DriverReportAdmin(admin.StackedInline):
    model = DriverReport
    extra = 0
    max_num = 0
    can_delete = False
    readonly_fields = (
        "driver",
        "total_working_hours",
        "driver_trip_count",
        "driver_amount",
    )


class HireTripsReportAdmin(admin.TabularInline):
    model = HireTripReport
    extra = 0
    max_num = 0
    readonly_fields = ("driver", "trip_date", "trip_status", "trip_hours")
    exclude = ("trip_id",)
    can_delete = False

    def trip_date(self, obj):
        return obj.trip_id.trip_date

    def trip_status(self, obj):
        return obj.trip_id.trip_status

    def trip_hours(self, obj):
        return obj.trip_id.trip_hours


class HireusReportAdmin(admin.ModelAdmin):
    list_display = ("report_title",)
    readonly_fields = ("trip_count", "trip_attended", "amount_per_day", "total_amount")

    def get_inlines(self, request, obj=None):
        if obj:
            return [DriverReportAdmin, HireTripsReportAdmin]
        else:
            return []

    def save_model(self, request, obj, form, change):
        # drop_time  = form.cleaned_data.get('drop_time')
        hire_id = form.cleaned_data.get("hire")
        hire = HireUs.objects.get(id=hire_id.id)
        print(obj.id)
        if hire:
            trip_count = hire.hire_trips.all().count()  # type: ignore
            trip_attended = hire.hire_trips.filter(trip_status=True).count()  # type: ignore

            obj.trip_count = trip_count
            obj.trip_attended = trip_attended
            obj.amount_per_day = hire.amount_per_day
            obj.total_amount = trip_attended * hire.amount_per_day

        # trip_status = form.cleaned_data.get("-trip_status")
        # amount_status = form.cleaned_data.get("amount_status")
        # if not obj.drop_time:  # type: ignore
        #     if trip_status == "COMPLETED":
        #         obj.drop_time = timezone.now()  # type: ignore

        update_fields = []

        # if change:
        #     if form.initial["amount_status"] != form.cleaned_data["amount_status"]:
        #         update_fields.append("amount_status")

        super().save_model(request, obj, form, change)
        obj.save(update_fields=update_fields)


admin.site.register(HireUs, HireUsAdmin)
admin.site.register(HireusReport, HireusReportAdmin)
