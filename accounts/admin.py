from django import forms
from django.contrib import admin

from .models import Customer, Driver, MyUser, DriverProfile, CustomerProfile


# Register your models here.

class CustomerProfileAdmin(admin.ModelAdmin):
    model=CustomerProfile


class DriverProfileAdmin(admin.StackedInline):
    model=DriverProfile

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
        )
        required = ("first_name",)
        
     


class DriverForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
        )
        required = ("first_name",)
       


class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
    list_display = ("phone", "first_name", "last_name", "is_customer")
    list_filter = ("date_joined",)
    ordering=['date_joined']
    search_fields = ("phone", "first_name", "last_name", "email")

    def get_inlines(self, request, obj=None):
        if obj:
            return [CustomerProfileAdmin]
        else:
            return []


class DriverAdmin(admin.ModelAdmin):
    form = DriverForm
    list_display = ("phone", "first_name", "last_name", "is_driver")
    list_filter = ("date_joined",)
    search_fields = ("phone", "first_name", "last_name", "email")

    def get_inlines(self, request, obj=None):
        if obj:
            return [DriverProfileAdmin]
        else:
            return []

class UserAdmin(admin.ModelAdmin):
    list_display = (
        "phone",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_driver",
        "is_customer",
    )
    list_filter = (
        "date_joined",
        "is_staff",
        "is_superuser",
        "is_driver",
        "is_customer",
    )
    search_fields = ("phone", "first_name", "last_name", "email")


admin.site.register(MyUser, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Driver, DriverAdmin)
