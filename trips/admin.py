from django.contrib import admin
from django import forms
from django.http import HttpResponseRedirect
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory, MoveNodeForm
from .models import Trip, TripType
from .utils import gernerate_message
from django.utils import timezone

from dal import autocomplete

from wallets.models import DriverWalletTransaction




# Register your models here.
class MyNodeForm(MoveNodeForm):
    class Meta:
        model = TripType
        exclude = ("sib_order", "parent")


class TripForm(forms.ModelForm):
    driver_based_on_loaction = forms.BooleanField(
        widget=forms.CheckboxInput(),
        label="Driver Based location",
        help_text="This will turn on/off location based on driver selection",
        required=False,
    )

    trip_parent_type = forms.ModelChoiceField(
        queryset=TripType.objects.filter(depth=1),
    )

    class Meta:
        model = Trip
        fields = "__all__"
        widgets = {
            "driver": autocomplete.ModelSelect2(
                "driver-autocomplete",
                forward=["pickup_area", "driver_based_on_loaction"],
            ),
            "trip_type": autocomplete.ModelSelect2(
                "triptype-autocomplete",
                forward=[
                    "trip_parent_type",
                ],
            ),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        super(TripForm, self).__init__(*args, **kwargs)
        if instance:
            child_id = self.instance.trip_type.id
            self.fields["trip_parent_type"].initial = (
                TripType.objects.get(pk=child_id).get_parent().id
            )
        else :
            local_trip = TripType.objects.all().first()
            if local_trip:
                self.fields["trip_parent_type"].initial = (local_trip.id)
                child_trip =  local_trip.get_children().first()
                self.fields["trip_type"].initial = (child_trip.id)
        self.fields["driver_based_on_loaction"].initial = True


# trip actions
@admin.action(description="Mark selected trip as completed")
def make_trip_completed(modeladmin, request, queryset):
    queryset.update(trip_status="COMPLETED", drop_time=timezone.now())


@admin.action(description="Mark selected trip amount as paid")
def make_amount_paid(modeladmin, request, queryset):
    for obj in queryset:
        if obj.amount_status != "PAID":
            obj.amount_status = "PAID"
            obj.save(update_fields=["amount_status"])
        obj.save()


@admin.action(description="Mark selected trip as completed and amount as paid")
def make_trip_completed_amount_paid(modeladmin, request, queryset):
    # queryset.update(
    #     trip_status="COMPLETED", drop_time=timezone.now(), amount_status="PAID"
    # )

    for obj in queryset:
        if obj.trip_status != "COMPLETED":
            obj.trip_status = "COMPLETED"
            obj.drop_time = timezone.now()
        if obj.amount_status != "PAID":
            obj.amount_status = "PAID"
            obj.save(update_fields=["amount_status"])
        obj.save()


class TripAdmin(admin.ModelAdmin):
    change_form_template = "admin/trips/change_form.html"

    form = TripForm

    list_display = (
        "trip_id",
        "customer",
        "customer_contact",
        "pickup_location",
        "pickup_time",
        "drop_location",
        "driver",
        "driver_contact",
        "amount",
        "amount_status",
    )
    search_fields = ["customer_phone", "trip_id"]
    autocomplete_fields = ["customer"]
    readonly_fields = ("created_at", "updated_at", "drop_time")
    list_filter = ("trip_status", "amount_status")
    ordering = ("trip_status",)
    actions = (make_trip_completed, make_amount_paid, make_trip_completed_amount_paid)

    fieldsets = (
        ("Customer", {"fields": ("customer",)}),
        (
            "Trip Details",
            {
                "fields": (
                    "trip_parent_type",
                    "trip_type",
                    "pickup_area",
                    "pickup_location",
                    "pickup_time",
                    "drop_location",
                    "drop_time",
                    "landmark",
                )
            },
        ),
        (
            "Driver Details",
            {"fields": ("driver", "driver_based_on_loaction")},
        ),
        (
            "Payment Details / Status",
            {"fields": ("amount", "amount_status", "trip_status")},
        ),
    )

    @admin.display(ordering="customer__phone", description="Customer contact")
    def customer_contact(self, obj):
        return obj.customer.phone

    @admin.display(ordering="driver__phone", description="Driver contact")
    def driver_contact(self, obj):
        if obj.driver:
            return obj.driver.phone
        return None
    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)

        formfield.widget.can_delete_related = False  # type: ignore

        # formfield.widget.can_add_related = False  # can change this, too
        # formfield.widget.can_view_related = False  # can change this, too

        return formfield

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'trip_type':
    #         CHOICES = MoveNodeForm.mk_dropdown_tree(TripType)
    #         return ChoiceField(choices=CHOICES)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # @admin.action(description='Mark selected trip as completed')
    # def make_published(modeladmin, request, queryset):
    #     queryset.update(trip_status='COMPLETED', drop_time=timezone.now())

    def save_model(self, request, obj, form, change):
        # drop_time  = form.cleaned_data.get('drop_time')

        trip_status = form.cleaned_data.get("-trip_status")
        amount_status = form.cleaned_data.get("amount_status")
        if not obj.drop_time:  # type: ignore
            if trip_status == "COMPLETED":
                obj.drop_time = timezone.now()  # type: ignore

        update_fields = []

        if change:
            if form.initial["amount_status"] != form.cleaned_data["amount_status"]:
                update_fields.append("amount_status")

        super().save_model(request, obj, form, change)
        obj.save(update_fields=update_fields)

    def change_view(self, request, object_id, form_url="", extra_content={}):
        data = self.get_queryset(request).get(pk=object_id)

        if data:
            local_time = timezone.localtime(data.pickup_time)
            date = local_time.strftime("%d/%m/%y")
            time = local_time.strftime("%I:%M %p")
            driver_name = data.driver.get_full_name() if data.driver else ''
            driver_phone =   data.driver.phone if data.driver else ''
            c_message = gernerate_message(
                data.customer.get_full_name(),
                data.customer.phone,
                data.trip_type.name,
                data.drop_location,
                date,
                time,
                driver_name,
                driver_phone,
                data.trip_id,
                data.pickup_location,
                False,
            )
            d_message = gernerate_message(
                data.customer.get_full_name(),
                data.customer.phone,
                data.trip_type.name,
                data.drop_location,
                date,
                time,
                driver_name,
                driver_phone,
                data.trip_id,
                data.pickup_location,
                True,
            )
            extra_content.update({"c_message": c_message})
            extra_content.update({"d_message": d_message})
            extra_content.update({"customer": f"+91{data.customer.phone}"})
            extra_content.update({"driver": f"+91{driver_phone}"})

        return super().change_view(request, object_id, form_url, extra_content)


# CHOICES = MoveNodeForm.mk_dropdown_tree(Category)
# category = ChoiceField(choices=CHOICES)


class TripTypeAdmin(TreeAdmin):
    readonly_fields = ("slug", "created_at", "updated_at")
    form = movenodeform_factory(TripType)


admin.site.register(Trip, TripAdmin)
admin.site.register(TripType, TripTypeAdmin)
