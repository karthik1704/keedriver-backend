from datetime import date, timedelta

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from rangefilter.filters import (  # DateTimeRangeFilterBuilder,; NumericRangeFilterBuilder,
    DateRangeFilterBuilder,
)

from cars.models import Car
from reviews.models import Review

from .models import (
    BlockDriver,
    Customer,
    CustomerProfile,
    Driver,
    DriverProfile,
    MyUser,
)

# Register your models here.


class CustomerProfileAdmin(admin.StackedInline):
    model = CustomerProfile


class DriverProfileAdmin(admin.StackedInline):
    model = DriverProfile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "driver"


class CustomerReviews(admin.StackedInline):
    model = Review
    can_delete = False
    extra = 0
    fk_name = "review_to"
    max_num = 0
    classes = ("collapse",)
    readonly_fields = (
        "trip",
        "reviewer",
        "rating",
        "title",
        "comment",
    )


class DriverReviews(admin.StackedInline):
    model = Review
    can_delete = False
    extra = 0
    fk_name = "review_to"
    max_num = 0
    classes = ("collapse",)
    readonly_fields = (
        "trip",
        "reviewer",
        "rating",
        "title",
        "comment",
    )


class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields["phone"].help_text = (
            "only enter 10 digits phone number, should not contain '+91' and spaces"
        )

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
    def __init__(self, *args, **kwargs):
        super(DriverForm, self).__init__(*args, **kwargs)
        self.fields["phone"].help_text = (
            "only enter 10 digits phone number, should not contain '+91' and spaces"
        )

    class Meta:
        model = Driver
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
        )
        required = ("first_name",)


class BlockDriverInline(admin.TabularInline):
    model = BlockDriver
    extra = 0
    fk_name = "blocker"
    autocomplete_fields = [
        "blocked_user",
    ]

    classes = ("collapse",)


class CarInline(admin.StackedInline):
    model = Car
    extra = 0


class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
    list_display = ("phone", "first_name", "last_name", "is_customer")
    list_filter = (
        "date_joined",
        ("date_joined", DateRangeFilterBuilder()),
    )
    ordering = ["date_joined"]
    search_fields = ("phone", "first_name", "last_name", "email")

    def get_inlines(self, request, obj=None):
        if obj:
            return [CustomerProfileAdmin, CustomerReviews, BlockDriverInline, CarInline]
        else:
            return []

    readonly_fields = ("formatted_overall_rating",)

    def formatted_overall_rating(self, obj):
        overall_rating = obj.overall_rating
        if overall_rating is not None:
            return f"{overall_rating:.1f}"
        return "N/A"

    formatted_overall_rating.short_description = "Overall Rating"


class DriverAdmin(admin.ModelAdmin):
    form = DriverForm
    inlines = (DriverProfileAdmin, DriverReviews)

    list_display = (
        "phone",
        "first_name",
        "last_name",
        "driver_exp_date",
        "is_driver",
        "date_joined",
    )
    list_filter = ("date_joined", ("date_joined", DateRangeFilterBuilder()))
    search_fields = ("phone", "first_name", "last_name", "email")
    fieldsets = (
        (
            "Driver Information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "formatted_overall_rating",
                ),
            },
        ),
    )

    readonly_fields = ("formatted_overall_rating",)

    def formatted_overall_rating(self, obj):
        overall_rating = obj.overall_rating
        if overall_rating is not None:
            return f"{overall_rating:.1f}"
        return "N/A"

    formatted_overall_rating.short_description = "Overall Rating"

    # def get_inlines(self, request, obj=None):
    #     if obj:
    #         return [DriverProfileAdmin]
    #     else:
    #         return []

    @admin.display(
        ordering="driverprofile__license_expiry_date", description="license exp date"
    )
    def driver_exp_date(self, obj):
        if obj.driverprofile:
            expiry_date = obj.driverprofile.license_expiry_date
            if expiry_date <= date.today():
                return format_html(
                    '<b style="color:{};">{}</b>',
                    "red",
                    expiry_date.strftime("%b, %d, %Y"),
                )
            return format_html(
                '<b style="color:{};">{}</b>',
                "green",
                expiry_date.strftime("%b, %d, %Y"),
            )

    # def response_add(self, request: HttpRequest, obj: _ModelT, post_url_continue: Optional[str] = ...) -> HttpResponse:
    #     return super().response_add(request, obj, post_url_continue)
    # def response_add(self, request, obj, post_url_continue=None):
    #     if '_continue' not in request.POST:
    #         return HttpResponseRedirect("../%s" % obj.id)
    #     else:
    #         return super(DriverAdmin, self).response_add(request, obj, post_url_continue)

    # def driver_exp_date(self, obj):

    #     return format_html(
    #         '<b style="color:{};">{}</b>',
    #         'red',
    #         obj.driverprofile.license_expiry_date,
    #     )


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
        (
            "Account Information",
            {
                "fields": ("username", "phone", "email", "password"),
            },
        ),
        (
            "Personal Information",
            {
                "fields": ("first_name", "last_name", "country"),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_driver",
                    "is_customer",
                ),
            },
        ),
        (
            "Log Information",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": ("username", "email", "phone", "password1", "password2"),
            },
        ),
        (
            "Personal Information",
            {
                "fields": ("first_name", "last_name", "country"),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_driver",
                    "is_customer",
                ),
            },
        ),
    )

    readonly_fields = ("last_login", "date_joined")
    search_fields = ("username", "phone", "first_name", "last_name", "email")

    def get_form(self, request, obj=None, **kwargs):
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["username"].required = True
        return form


admin.site.register(MyUser, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Driver, DriverAdmin)
