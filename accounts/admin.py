from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import Group

from .models import Customer, Driver, MyUser, DriverProfile, CustomerProfile


# Register your models here.

class CustomerProfileAdmin(admin.StackedInline):
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
        model = Driver
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

class UserAdmin(AuthUserAdmin):
    model = MyUser
    list_display = (
        "phone",
        "username",
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

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        ('Account Information', {
            'fields': ('username','phone','email',  'password'),
        }),
        ('Personal Information', {
            'fields': ('first_name','last_name', 'country'),
        }),
        ('Permissions', {
            'fields': ('is_active','is_staff','is_superuser',"is_driver",
        "is_customer",  ),
        }),
         ('Log Information', {
            'fields': ("last_login",'date_joined',),
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username','email', 'phone', 'password1', 'password2'),
        }),
        ('Personal Information', {
            'fields': ('first_name','last_name', 'country'),
        }),
        ('Permissions', {
            'fields': ('is_active','is_staff','is_superuser',"is_driver",
        "is_customer",),
        }),
    )
    
    readonly_fields= ("last_login",'date_joined')
    search_fields = ("phone", "first_name", "last_name", "email")

    def get_form(self, request, obj=None, **kwargs):
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['username'].required = True
        return form

admin.site.register(MyUser, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Driver, DriverAdmin)
