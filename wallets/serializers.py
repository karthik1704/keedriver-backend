from rest_framework import serializers

from .models import DriverWallet, DriverWalletTransaction

from accounts.serializers import DriverSerializer



class DriverWalletSerializer(serializers.ModelSerializer):
    driver_name = serializers.SerializerMethodField( read_only=True)

    class Meta:
        model = DriverWallet
        fields='__all__'
        # depth=1
    def get_driver_name(self, obj):
        return obj.driver.get_full_name()

class DriverWalletTransactionSerializer(serializers.ModelSerializer):
    driver_name = serializers.SerializerMethodField( read_only=True)
    trip_id = serializers.SerializerMethodField( read_only=True)

    class Meta:
        model = DriverWalletTransaction
        fields = "__all__"

    def get_driver_name(self, obj):
        return obj.wallet.driver.get_full_name()
    
    def get_trip_id(self, obj):

        if obj.trip:
            return obj.trip.trip_id
        return None