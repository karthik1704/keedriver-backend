from django.contrib import admin
from django.forms import ChoiceField
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory, MoveNodeForm
from .models import Trip, TripType

# Register your models here.
class MyNodeForm(MoveNodeForm):
    class Meta:
        model = TripType
        exclude = ('sib_order', 'parent')

class TripAdmin(admin.ModelAdmin):
    list_display = (
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
    search_fields = ['customer_phone']
    autocomplete_fields = ['customer', 'driver']
    readonly_fields = ("created_at", "updated_at")
    list_filter = ('trip_status',)
    ordering=("trip_status",)

    fieldsets = (
        ("Customer", {"fields": ("customer",)}),
        (
            "Trip Details",
            {
                "fields": (
                    "trip_type",
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
            {"fields": ("driver",)},
        ),
        (
            "Payment Details / Status",
            {
                "fields": (
                    "amount",
                    "amount_status",
                    "trip_status"
                )
            },
        ),
    )

    @admin.display(ordering="customer__phone", description="Customer contact")
    def customer_contact(self, obj):
        return obj.customer.phone

    @admin.display(ordering="driver__phone", description="Driver contact")
    def driver_contact(self, obj):
        return obj.driver.phone

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)

        formfield.widget.can_delete_related = False  # type: ignore

        # formfield.widget.can_add_related = False  # can change this, too
        # formfield.widget.can_view_related = False  # can change this, too

        return formfield

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'trip_type':
            CHOICES = MoveNodeForm.mk_dropdown_tree(TripType)
            return ChoiceField(choices=CHOICES)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# CHOICES = MoveNodeForm.mk_dropdown_tree(Category)
# category = ChoiceField(choices=CHOICES)

class TripTypeAdmin(TreeAdmin):
    readonly_fields = ("slug", "created_at", "updated_at")
    form = movenodeform_factory(TripType)


admin.site.register(Trip, TripAdmin)
admin.site.register(TripType, TripTypeAdmin)
