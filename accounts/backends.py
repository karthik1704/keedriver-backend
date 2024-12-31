import re

from annotated_types import T
from django.contrib.auth.backends import ModelBackend

from .models import MyUser

"""
This is a custom authentication backend that allows users to log in using their phone number.
"""


class PasswordlessBackend(ModelBackend):

    def authenticate(self, request, phone=None, role=None, **kwargs):

        user = None
        try:
            user = MyUser.objects.get(phone=phone)
            return user
        except MyUser.DoesNotExist:
            if role is None:
                return None
            if role == "customer":
                user = MyUser.objects.create(
                    phone=phone, first_name="", is_active=True, is_customer=True
                )
                return user
            if role == "driver":
                # user = MyUser.objects.create(
                #     phone=phone, first_name="", is_active=False, is_driver=True
                # )
                # return user
                return None

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            return None
