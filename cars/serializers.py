from urllib import request
from rest_framework import serializers

# from asyncore import read
from cars.models import Car, CarEngineType, CarType


class CarCreateSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Car
        exclude =('customer',)

    



class CarReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class CarDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class CarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        exclude =('customer',)


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
