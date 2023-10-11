from rest_framework import serializers

from hire_us.models import DriverReport, HireTripReport, HireTrips, HireUs, HireusReport


class HireTripsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HireTrips
        fields = "__all__"


class HireUsSerializer(serializers.ModelSerializer):
    hire_trips = HireTripsSerializer(
        many=True,
    )

    class Meta:
        model = HireUs
        fields = "__all__"


class HireTripsReportSerializer(serializers.ModelSerializer):
    trip_id = HireTripsSerializer(read_only=True)

    class Meta:
        model = HireTripReport
        fields = "__all__"


class DriverReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverReport
        fields = "__all__"


class HireUsReportSerializer(serializers.ModelSerializer):
    hire_trip_report = HireTripsReportSerializer(many=True, read_only=True)
    driver_report = DriverReportSerializer(many=True, read_only=True)

    class Meta:
        model = HireusReport
        fields = "__all__"
        read_only_fields = (
            "trip_count",
            "trip_attended",
            "amount_per_day",
            "total_amount",
        )

    def validate(self, attrs):
        print(attrs.get("billing_start_date"))
        start_date = attrs["billing_start_date"]
        end_date = attrs["billing_end_date"]
        hire = attrs["hire"]
        trips = hire.hire_trips.filter(  # type:ignore
            trip_date__gte=start_date, trip_date__lte=end_date
        )
        trip_count = trips.count()
        date_invoiced = []
        date_processing = []
        date_draft = []
        for trip in trips:
            if trip.trip_status == "INVOICED":
                date_invoiced.append(trip.trip_date)
            if trip.trip_status == "INPROCESS":
                date_processing.append(trip.trip_date)
            if trip.trip_status == "DRAFT":
                date_draft.append(trip.trip_date)

        if attrs["amount_status"] == "DRAFT":
            if trip_count == 0:
                raise serializers.ValidationError(f"No trips found in between dates")
            if date_invoiced:
                raise serializers.ValidationError(
                    f'These date already invoiced {",".join(map(str, date_invoiced))}'
                )
            if date_processing:
                raise serializers.ValidationError(
                    f"""These date still InProcess - please update the date or change date  
                    {",".join(map(str, date_processing))}"""
                )
            if date_draft:
                raise serializers.ValidationError(
                    f"""These date still Draft - please update the date or change date  
                    {",".join(map(str, date_draft))}"""
                )

        return super().validate(attrs)
