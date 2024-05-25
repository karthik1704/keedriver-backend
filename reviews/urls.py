from django.urls import path
from .views import ReviewByTripId,ReviewCreateTripId,ReviewPutTrip,ReviewDeleteTrip

urlpatterns = [
    path('review/<int:trip_id>/',ReviewByTripId.as_view()),
    path('review/create/',ReviewCreateTripId.as_view()),
    path('review/<int:pk>/update/',ReviewPutTrip.as_view()),
    path('review/<int:pk>/delete/',ReviewDeleteTrip.as_view()),

]