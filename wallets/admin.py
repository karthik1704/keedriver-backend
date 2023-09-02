from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin, ExportMixin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from rangefilter.filters import (
    DateRangeFilterBuilder,
    # DateTimeRangeFilterBuilder,
    # NumericRangeFilterBuilder,
)

from .models import DriverWallet, DriverWalletTransaction
# Register your models here.

class DriverWalletAdmin(admin.ModelAdmin):

    list_display =('driver', 'amount')

class DriverWalletTransactionResource(resources.ModelResource):
 
    trip_id =  Field(
        attribute="trip__trip_id", column_name="trip_id", readonly=True
    )
    driver_first_name = Field(
        attribute="wallet__driver__first_name", column_name="driver_first_name", readonly=True
    )
    driver_last_name = Field(
        attribute="wallet__driver__last_name", column_name="driver_last_name", readonly=True
    )
    driver_phone = Field(
        attribute="wallet__driver__phone",
        column_name="driver_phone",
        readonly=True
    )

   

    class Meta:
        model = DriverWalletTransaction
        exclude = ('trip', 'wallet')
        export_order = (
            "id",
            "trip_id",
            "driver_first_name",
            "driver_last_name",
            "driver_phone",
        )


class DriverWalletTransactionAdmin(ExportActionMixin, ExportMixin ,admin.ModelAdmin):
    import_export_change_list_template = (
        "admin/import_export/change_list_import_export.html"
    )
    resource_classes = [DriverWalletTransactionResource]
    list_display = ('wallet', 'trip', 'transaction_type', "amount", "transaction_date" )
    list_filter = (('transaction_date', DateRangeFilterBuilder()),)
    search_fields = ('trip__trip_id', 'wallet__driver__phone')

admin.site.register(DriverWallet, DriverWalletAdmin)
admin.site.register(DriverWalletTransaction, DriverWalletTransactionAdmin)

