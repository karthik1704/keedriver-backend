from django import forms
from django.contrib import admin

from .models import Customer, Driver, MyUser


# Register your models here.
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


class DriverAdmin(admin.ModelAdmin):
    form = DriverForm
    list_display = ("phone", "first_name", "last_name", "is_driver")
    list_filter = ("date_joined",)
    search_fields = ("phone", "first_name", "last_name", "email")


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
