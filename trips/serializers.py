from typing import Union

from rest_framework import serializers

from accounts.models import Driver
from accounts.serializers import CustomerSerializer, DriverSerializer
from cars.models import Car
from cars.serializers import CarSerializer

from .models import Trip, TripType


class TripTypeChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripType
        exclude = (
            "path",
            "depth",
            "numchild",
        )


class TripTypeSerializer(serializers.ModelSerializer):
    children = TripTypeChildrenSerializer(many=True, read_only=True)
    # parent_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = TripType
        exclude = (
            "path",
            "depth",
            "numchild",
        )


class TripTypeDetailSerializer(TripTypeSerializer):
    children = TripTypeChildrenSerializer(many=True, read_only=True)
    parent = TripTypeSerializer(read_only=True)

    class Meta:
        model = TripType
        exclude = (
            "path",
            "depth",
            "numchild",
        )

    # def get_children(self, obj):

    #     return obj.get_children()

    # def get_parent(self, obj):
    #     return obj.get_parent().id if obj.get_parent() else None


class TripTypeUpdateSerializer(serializers.ModelSerializer):
    parent_id = serializers.CharField(allow_null=True)

    class Meta:
        model = TripType
        exclude = (
            "path",
            "depth",
            "numchild",
        )

    # def update(self, instance, validated_data):
    #     parent_id = validated_data.get("parent_id")
    #     slug = validated_data.get("slug")
    #     name = validated_data.get("name")
    #     print(parent_id)
    #     if parent_id:
    #         parent = TripType.objects.get(pk=parent_id)
    #         print(parent)
    #         parent.move(instance,  pos=None)

    #     return instance


class TripTypeCreateSerializer(TripTypeSerializer):
    parent_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = TripType
        exclude = (
            "path",
            "depth",
            "numchild",
        )

    def create(self, validated_data):
        parent_id = validated_data.get("parent_id")
        slug = validated_data.get("slug")
        name = validated_data.get("name")
        if parent_id:
            parent = TripType.objects.get(pk=parent_id)
            return parent.add_child(name=name, slug=slug)
        return TripType.add_root(name=name, slug=slug)


class TripSerializer(serializers.ModelSerializer):
    driver_name = serializers.SerializerMethodField(read_only=True)
    customer_name = serializers.SerializerMethodField(read_only=True)
    car = CarSerializer(read_only=True)
    trip_type = TripTypeSerializer(read_only=True)

    class Meta:
        model = Trip
        fields = "__all__"
        read_only_fields = ("driver_name", "customer_name", "car")

    def get_driver_name(self, obj) -> Union[str, None]:
        if obj.driver:
            return obj.driver.get_full_name()
        return None

    def get_customer_name(self, obj) -> Union[str, None]:
        return obj.customer.get_full_name()


class CustomerTripSerializer(serializers.ModelSerializer):
    driver_name = serializers.SerializerMethodField(read_only=True)
    customer_name = serializers.SerializerMethodField(read_only=True)
    car = CarSerializer(read_only=True)  # For retrieval
    car_id = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(), source="car", write_only=True
    )
    trip_type = TripTypeSerializer(read_only=True)
    trip_type_id = serializers.PrimaryKeyRelatedField(
        queryset=TripType.objects.all(), source="trip_type", write_only=True
    )
    driver = DriverSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Trip
        fields = "__all__"
        read_only_fields = (
            "trip_status",
            "amount",
            "amount_status",
            "driver",
            "customer",
            "drop_time",
            "pickup_area",
        )

    def get_driver_name(self, obj) -> Union[str, None]:
        if obj.driver:
            return obj.driver.get_full_name()
        return None

    def get_customer_name(self, obj) -> Union[str, None]:
        return obj.customer.get_full_name()


class TripStatusUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = "__all__"
        extra_kwargs = {
            field.name: {"read_only": True}
            for field in Trip._meta.get_fields()
            if field.name != "trip_status"
        }


## Dashboard


class TripDashboardSerializer(serializers.Serializer):

    class Meta:
        fields = "__all__"
