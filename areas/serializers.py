from rest_framework import serializers

from .models import City , Area



class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    area = AreaSerializer(many=True, read_only=True)
    class Meta:
        model = City
        fields = ('id','name', 'area',)

    
        

