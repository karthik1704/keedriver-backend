from django.urls import path

from .views import CreateReview, ReviewByTripId

urlpatterns = [
    path("review/<int:trip_id>/", ReviewByTripId.as_view()),
    path("review/create/", CreateReview.as_view()),
]
