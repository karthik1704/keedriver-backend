from django.contrib import admin

from cars.models import Car, CarEngineType, CarType

# Register your models here.
admin.site.register(CarType)
admin.site.register(CarEngineType)
admin.site.register(Car)
