from django.contrib.auth.models import BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, phone, password=None):

        if not password:
            raise ValueError("Password is must !")

        user = self.model(
            username=username,
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone, password):
        user = self.create_user(
            username=username,
            phone=phone,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomerManager(models.Manager):
    def create_user(self, email, phone, password=None):
        if not phone or len(phone) <= 0:
            raise ValueError("Phone field is required !")

        email = email.lower()
        user = self.model(email=email, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_customer=True)
        return queryset


class DriverManager(models.Manager):
    def create_user(self, email, phone, password=None):
        if not phone or len(phone) <= 0:
            raise ValueError("Phone field is required !")

        email = email.lower()
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_driver=True)
        return queryset
