from django.contrib import admin

from reviews.models import Review


# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    autocomplete_fields = ("reviewer", "review_to")


admin.site.register(Review, ReviewAdmin)
