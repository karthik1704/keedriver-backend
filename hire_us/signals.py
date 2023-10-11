from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from accounts.models import Driver
from trips.models import DEDUCTION_PERCENTAGE
from wallets.models import DriverWallet, DriverWalletTransaction

from .models import DriverReport, HireTripReport, HireTrips, HireUs, HireusReport


@receiver(post_save, sender=HireUs)
def add_hire_id(sender, instance, created, **kwargs):
    if created:
        year = instance.created_at.strftime("%Y")
        id = str(instance.id)
        hire_id = f"KDH{year}{id}"
        instance.hire_id = hire_id

        # create hire trips
        driver = instance.driver
        start_date = instance.start_date
        end_date = instance.end_date
        include_saturday = instance.include_saturday
        include_sunday = instance.include_sunday
        while start_date <= end_date:
            weekday = start_date.isoweekday()
            if not weekday == 7 and not weekday == 6:
                HireTrips.objects.create(
                    hire=instance, driver=driver, trip_date=start_date
                )

            if include_saturday and weekday == 6:
                HireTrips.objects.create(
                    hire=instance, driver=driver, trip_date=start_date
                )

            if include_sunday and weekday == 7:
                HireTrips.objects.create(
                    hire=instance, driver=driver, trip_date=start_date
                )

            start_date += timezone.timedelta(days=1)
        instance.save()

        if not created:
            updated = kwargs.get("update_fields")
            print(updated)


@receiver(post_save, sender=HireTrips)
def updating_hire_trips(sender, instance, created, **kwargs):
    if not created:
        updated = kwargs.get("update_fields")
        print(updated, "53")


@receiver(post_save, sender=HireusReport)
def add_driver_reports(sender, instance, created, **kwargs):
    if created:
        hire_id = instance.hire
        start_date = instance.billing_start_date
        end_date = instance.billing_end_date

        hire = HireUs.objects.get(id=hire_id.id)
        trips = hire.hire_trips.filter(  # type:ignore
            trip_date__gte=start_date, trip_date__lte=end_date, trip_status="COMPLETED"
        )
        trip_drivers = trips.order_by().values("driver").distinct()  # type: ignore
        print(trip_drivers)

        for drivers in trip_drivers:
            print(drivers["driver"])
            driver_id = drivers["driver"]
            driver = Driver.objects.get(id=driver_id)
            if driver:
                driver_trips_count = trips.filter(driver=driver_id).count()
                print(f"this {driver_trips_count}")
                total = (
                    trips.filter(driver=driver_id).aggregate(Sum("trip_hours"))[
                        "trip_hours__sum"
                    ]
                    or timezone.timedelta()
                )

                trips_amount = hire.amount_per_day * driver_trips_count
                percentange_amount = hire.driver_cut_percentage / 100 * trips_amount
                driver_amount = trips_amount - percentange_amount
                driver_report = DriverReport.objects.create(
                    report=instance,
                    driver=driver,
                    total_working_hours=total,
                    driver_trip_count=driver_trips_count,
                    driver_amount=driver_amount,
                )
                driver_report.save()
                driver_trips = trips.filter(driver=driver_id)
                for trip in driver_trips:
                    trip_report = HireTripReport.objects.create(
                        report=instance, trip_id=trip
                    )

        # for trip in trips:
        #     trip.trip_status = "INVOICED"
        #     trip.save()

    # if not created:
    #     hire_id = instance.hire
    #     start_date = instance.billing_start_date
    #     end_date = instance.billing_end_date

    #     hire = HireUs.objects.get(id=hire_id.id)
    #     trips = hire.hire_trips.filter(  # type:ignore
    #         trip_date__gte=start_date, trip_date__lte=end_date
    #     )
    #     trip_drivers = trips.order_by().values("driver").distinct()  # type: ignore
    #     print(trip_drivers)
    #     for drivers in trip_drivers:
    #         print(drivers["driver"])
    #         driver_id = drivers["driver"]
    #         driver = Driver.objects.get(id=driver_id)
    #         if driver:
    #             driver_trips_count = trips.filter(driver=driver_id).count()
    #             total = (
    #                 trips.filter(driver=driver_id).aggregate(Sum("trip_hours"))[
    #                     "trip_hours__sum"
    #                 ]
    #                 or timezone.timedelta()
    #             )
    #             print(total)
