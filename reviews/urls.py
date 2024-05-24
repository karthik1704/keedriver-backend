from django.urls import path
from .views import ReviewByTripId,ReviewCreateTripId

urlpatterns = [
    path('review/<int:trip_id>/',ReviewByTripId.as_view()),
    path('review/create/',ReviewCreateTripId.as_view()),

]