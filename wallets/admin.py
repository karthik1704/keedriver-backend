from django.contrib import admin

from .models import DriverWallet, DriverWalletTransaction
# Register your models here.

class DriverWalletAdmin(admin.ModelAdmin):

    list_display =('driver', 'amount')


class DriverWalletTransactionAdmin(admin.ModelAdmin):

    list_display = ('wallet', 'trip', 'transaction_type', "amount" )

admin.site.register(DriverWallet, DriverWalletAdmin)
admin.site.register(DriverWalletTransaction, DriverWalletTransactionAdmin)

