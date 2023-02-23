from django.contrib import admin
from django.db.models import Count


from .models import City, Area
# Register your models here.
class CityAdmin(admin.ModelAdmin):

    list_display= ("name", "areas_count", )


    @admin.display(description="Areas Count")
    def areas_count(self, obj):
        return obj.area_count
    

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(area_count=Count("area"))
        return queryset

class AreaAdmin(admin.ModelAdmin):

    list_display= ("name", "city", )


admin.site.register(City, CityAdmin)
admin.site.register(Area, AreaAdmin)