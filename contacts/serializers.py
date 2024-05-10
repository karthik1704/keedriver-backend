from rest_framework import serializers
from .models import contact

class ContactSerializers(serializers.ModelSerializer):
    class Meta:

        model = contact
        fields = '__all__'