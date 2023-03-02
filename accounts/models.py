from typing import Iterable, Optional

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomerManager, CustomUserManager, DriverManager
from areas.models import Area

# Create your models here.
class MyUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(
        _("Username"), unique=True, blank=True, null=True, max_length=250
    )
    email = models.EmailField(_("e-mail"), unique=True, blank=True, null=True)
    phone = models.CharField(
        _("phone number"),
        unique=True,
        max_length=30,
    )

    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), blank=True, null=True, max_length=50)
    country = models.CharField(_("country"), blank=True, null=True, max_length=5)

    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("last login"), auto_now=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff"), default=False)
    is_superuser = models.BooleanField(_("superuser"), default=False)

    is_customer = models.BooleanField(_("Customer"), default=False)
    is_driver = models.BooleanField(_("Driver"), default=False)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    # def get_email_field_name(self):
    #     return self.EMAIL_FIELD

    def get_full_name(self):
        return f"{self.first_name} {self.last_name if self.last_name  else ''}"

    def get_short_name(self):
        return self.first_name

    # def get_username(self):
    #     return self.username

    def __str__(self) -> str:
    
        return f"{self.first_name} {self.last_name if self.last_name  else ''}"


    # this methods are require to login super user from admin panel
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    # this methods are require to login super user from admin panel
    def has_module_perms(self, app_label):
        return self.is_superuser


class Customer(MyUser):
    class Meta:
        proxy = True

    objects = CustomerManager()

    def save(self, *args, **kwargs) -> None:
        self.is_customer = True
        super().save(*args, **kwargs)


class CustomerProfile(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    is_business = models.BooleanField(default=False)

class Driver(MyUser):
    class Meta:
        proxy = True

    objects = DriverManager()

    def save(self, *args, **kwargs) -> None:
        self.is_driver = True
        super().save(*args, **kwargs)

class DriverProfile(models.Model):
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE)
    address =  models.TextField(blank=True, null=True,)
    area= models.ManyToManyField(Area,blank=True)
    license_number = models.CharField(max_length=50, null=True, blank=True)
    aadhaar_number = models.CharField(max_length=20, null=True, blank=True)
    is_avaliable = models.BooleanField(default=False)
    
    def __str__(self):
        return self.driver.get_full_name()