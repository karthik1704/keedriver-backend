from rest_framework import serializers

from cars.models import Car, CarEngineType, CarType


class CarCreateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Car
        fields = "__all__"


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = "__all__"


class CarEngineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarEngineType
        fields = "__all__"


class CarSerializer(serializers.ModelSerializer):
    type = CarTypeSerializer(read_only=True)
    engine_model = CarEngineTypeSerializer(read_only=True)

    class Meta:
        model = Car
        fields = "__all__"
