# Generated by Django 4.2.4 on 2023-09-29 15:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hire_us', '0003_alter_hiretrips_trip_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hiretrips',
            options={'verbose_name': 'Hire Trip', 'verbose_name_plural': 'Hire Trips'},
        ),
        migrations.AlterField(
            model_name='hiretrips',
            name='trip_hours',
            field=models.DurationField(blank=True, default=datetime.timedelta(0), null=True),
        ),
    ]
