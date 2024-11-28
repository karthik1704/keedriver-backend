import email

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers

from accounts.utils import verify_totp

from .models import Customer, Driver, MyUser


class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    # email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    role = serializers.CharField(required=False, default="customer")
    password = serializers.CharField(
        style={"input_type": "password"}, required=False, allow_blank=True
    )
    otp = serializers.CharField(
        style={"input_type": "password"}, required=False, allow_blank=True
    )

    class Meta:
        model = MyUser
        fields = ["username", "phone", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def authenticate(self, **kwargs):
        return authenticate(self.context["request"], **kwargs)

    # def _validate_email(self, email, password):
    #     user = None

    #     if email and password:
    #         user = self.authenticate(email=email, password=password)
    #     else:
    #         msg = _('Must include "email" and "password".')
    #         raise exceptions.ValidationError(msg)

    #     return user

    def _validate_phone(self, phone, otp, role):
        user = None
        if phone:
            verified_otp = verify_totp(phone, otp)
            if not verified_otp:
                msg = _("Entered OTP is incorrect / Expired.")
                raise exceptions.ValidationError(msg)

            user = self.authenticate(phone=phone, role=role)
        else:
            msg = _('Must include "phone" and "otp".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get("username")
        email = attrs.get("email")
        phone = attrs.get("phone")
        password = attrs.get("password")
        otp = attrs.get("otp")
        role = attrs.get("role")

        # if email:
        #     user = self._validate_email(email, password)
        if phone:
            user = self._validate_phone(phone, otp, role)
        elif username:
            user = self._validate_username(username, password)
        else:
            msg = _('Must include "Username" or "phone" and "password".')
            raise exceptions.ValidationError(msg)

        if user:
            # if not user.is_active:
            #     msg = _("User account is disabled.")
            #     raise exceptions.ValidationError(msg)
            pass
        else:
            msg = _("Unable to log in with provided credentials.")
            raise exceptions.ValidationError(msg)

        attrs["user"] = user
        return attrs


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        read_only_fields = (
            "date_joined",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_customer",
            "is_driver",
            "phone",
        )
        exclude = ("groups", "user_permissions", "password")


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        read_only_fields = ("date_joined", "last_login")
        exclude = ("groups", "user_permissions")
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "email": {"required": False},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields.pop("password")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = MyUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomPasswordChangeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    password = serializers.CharField()
    new_confrim_password = serializers.CharField()

    def validate(self, attrs):
        if attrs["password"] != attrs["new_confrim_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone",
            "email",
            "country",
            "is_customer",
            "date_joined",
            "last_login",
        )
        read_only_fields = ("is_customer", "date_joined", "last_login")


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone",
            "email",
            "country",
            "is_driver",
            "date_joined",
            "last_login",
        )
        read_only_fields = ("is_driver", "date_joined", "last_login")


class SendOTPRequestSerializer(serializers.Serializer):
    phone = serializers.CharField()


class CreateAccountSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
