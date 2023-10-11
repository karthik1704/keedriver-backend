from __future__ import annotations

from typing import Any

from django import forms
from django.contrib import admin
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.utils import timezone
from django.utils.html import format_html

from accounts.models import Driver
from trips.models import DEDUCTION_PERCENTAGE

from .models import (
    DriverReport,
    HirePaymentReport,
    HireTripReport,
    HireTrips,
    HireUs,
    HireusReport,
)


# Register your models here.
class HireTripsForm(forms.ModelForm):
    class Meta:
        model = HireTrips
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.trip_status == "INVOICED":
            self.fields["trip_status"].required = False
            self.fields["trip_status"].widget.attrs["disabled"] = "disabled"


class HireTripsInline(admin.TabularInline):
    model = HireTrips
    extra = 0
    form = HireTripsForm
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
            return ("trip_hours",)

        return super().get_readonly_fields(request, obj)


class HireUsAdmin(admin.ModelAdmin):
    # change_form_template = "admin/hire_us/change_form1.html"

    list_display = (
        "customer",
        "hire_id",
        "pickup_location",
        "drop_location",
        "start_date",
        "end_date",
    )
    inlines = (HireTripsInline,)
    search_fields = ["customer_phone", "hire_id"]
    autocomplete_fields = ["customer", "pickup_area", "driver"]
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
                "fields": ("driver", "driver_cut_percentage"),
            },
        ),
        (
            "Amount Information",
            {
                "fields": ("amount_per_day",),
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

    # def response_change(self, request, obj):
    #     if "_report" in request.POST:
    #         report = HireusReport.objects.create(hire=obj, title="test")
    #         report.save()
    #         print(report.pk)
    #         return HttpResponseRedirect(".")
    #     return super().response_change(request, obj)


class DriverReportAdmin(admin.StackedInline):
    model = DriverReport
    extra = 0
    max_num = 0
    classes = ("collapse",)
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
    readonly_fields = ("trip_driver", "trip_date", "trip_status", "trip_hours")
    exclude = ("trip_id",)
    can_delete = False

    def trip_date(self, obj):
        return obj.trip_id.trip_date

    def trip_status(self, obj):
        return obj.trip_id.trip_status

    def trip_hours(self, obj):
        return obj.trip_id.trip_hours

    def trip_driver(self, obj):
        return obj.trip_id.driver.get_full_name()


class HireusReportAdmin(admin.ModelAdmin):
    list_display = ("report_title", "billing_start_date", "billing_end_date")
    readonly_fields = ("trip_count", "trip_attended", "amount_per_day", "total_amount")
    search_fields = [
        "hire",
    ]
    autocomplete_fields = [
        "hire",
    ]
    fieldsets = (
        (
            "Customer Information",
            {
                "fields": ("hire",),
            },
        ),
        (
            "Report Information",
            {
                "fields": (
                    "report_title",
                    "billing_start_date",
                    "billing_end_date",
                ),
            },
        ),
        (
            "Trip Information",
            {
                "fields": (
                    "trip_count",
                    "trip_attended",
                    "total_amount",
                    "amount_status",
                ),
            },
        ),
    )

    def get_inlines(self, request, obj=None):
        if obj:
            return [DriverReportAdmin, HireTripsReportAdmin]
        else:
            return []

    def get_readonly_fields(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> list[str] | tuple[Any, ...]:
        if obj and obj.billing_start_date and obj.billing_end_date:
            return (
                "billing_start_date",
                "billing_end_date",
                "trip_count",
                "trip_attended",
                "amount_per_day",
                "total_amount",
            )

        if obj is not ... and obj and obj.amount_status == "NOT PAID":
            return (
                "hire",
                "billing_start_date",
                "billing_end_date",
                "trip_count",
                "trip_attended",
                "amount_per_day",
                "total_amount",
            )

        if obj and obj.amount_status == "PAID":
            return (
                "hire",
                "report_title",
                "billing_start_date",
                "billing_end_date",
                "trip_count",
                "amount_status",
                "trip_attended",
                "amount_per_day",
                "total_amount",
            )

        return super().get_readonly_fields(request, obj)

    def has_delete_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        if obj is not ... and obj and obj.amount_status != "DRAFT":
            return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        if obj is not ... and obj and obj.amount_status == "PAID":
            return False
        return super().has_change_permission(request, obj)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def save_model(self, request, obj, form, change):
        # drop_time  = form.cleaned_data.get('drop_time')
        hire_id = form.cleaned_data.get("hire")
        start_date = form.cleaned_data.get("billing_start_date")
        end_date = form.cleaned_data.get("billing_end_date")
        hire = HireUs.objects.get(id=hire_id.id)

        if hire and not change:
            trip_count = hire.hire_trips.filter(trip_date__gte=start_date, trip_date__lte=end_date).count() | 0  # type: ignore
            trip_attended = hire.hire_trips.filter(trip_date__gte=start_date, trip_date__lte=end_date, trip_status="COMPLETED").count()  # type: ignore

            obj.trip_count = trip_count
            obj.trip_attended = trip_attended
            obj.amount_per_day = hire.amount_per_day
            obj.total_amount = trip_attended * hire.amount_per_day

        if change:
            if (
                form.initial["amount_status"] != form.cleaned_data["amount_status"]
                and form.cleaned_data["amount_status"] == "NOT PAID"
            ):
                s_date = obj.billing_start_date
                e_date = obj.billing_end_date
                trips = hire.hire_trips.filter(trip_date__gte=s_date, trip_date__lte=e_date, trip_status="COMPLETED")  # type: ignore
                print(trips)
                for trip in trips:
                    trip.trip_status = "INVOICED"
                    trip.save()

            if (
                form.initial["amount_status"] != form.cleaned_data["amount_status"]
                and form.cleaned_data["amount_status"] == "PAID"
            ):
                total_driver_amount = obj.driver_report.all().aggregate(
                    Sum("driver_amount")
                )["driver_amount__sum"]
                remaining_amount = obj.total_amount - total_driver_amount
                hire_amount = obj.total_amount

                hpr = HirePaymentReport.objects.create(
                    hire_report=obj,
                    hire_amount=hire_amount,
                    total_driver_amount=total_driver_amount,
                    remaining_amount=remaining_amount,
                )
                hpr.save()

        super().save_model(request, obj, form, change)


class HirePaymentReportAdmin(admin.ModelAdmin):
    readonly_fields = ("cut_percentage", "drivers", "payment_status")

    def drivers(self, obj):
        dr_list = [dr for dr in obj.hire_report.driver_report.all()]
        drivers_html = "<div>"
        for dr in dr_list:
            drivers_html += (
                f"<p>{dr.driver.get_full_name()} - {dr.driver_amount}</p><br />"
            )
        drivers_html += "</div>"
        return format_html(drivers_html)  # Customize the HTML as needed

    drivers.short_description = "Driver - Amount"

    def payment_status(self, obj):
        return obj.hire_report.amount_status

    def cut_percentage(self, obj):
        return obj.hire_report.cut_percentage

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        if obj is not ... and obj:
            return False

        return super().has_change_permission(request, obj)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...):
        return False


admin.site.register(HireUs, HireUsAdmin)
admin.site.register(HireusReport, HireusReportAdmin)
admin.site.register(HirePaymentReport, HirePaymentReportAdmin)
