# Generated by Django 5.0.6 on 2024-12-04 04:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('areas', '0002_alter_city_options'),
        ('trips', '0004_trip_from_lat_trip_from_lng_trip_to_lat_trip_to_lng_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='pickup_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='areas.area'),
        ),
    ]
