# Generated by Django 5.0.6 on 2024-12-04 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_blockdriver'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driverprofile',
            old_name='is_avaliable',
            new_name='is_available',
        ),
    ]